import asyncio
from ctypes import cast
from email.policy import default
import itertools
import json
import time
import aiohttp
from decouple import config
from aiolimiter import AsyncLimiter
from aioretry import (
    retry,
    # Tuple[bool, Union[int, float]]
    RetryPolicyStrategy,
    RetryInfo
)

from sqlalchemy import MetaData, create_engine, select
from sqlalchemy.orm import sessionmaker

from db.pegas_schema import pegas_schema

HTTP_REQ_PER_SEC = 30
DB_PAGE_SIZE = 50

limiter = AsyncLimiter(HTTP_REQ_PER_SEC, time_period=1)

def retry_policy(info: RetryInfo) -> RetryPolicyStrategy:
    return False, (info.fails - 1) % 10 + 1

API_BASE_URL = 'https://api-apollo.pegaxy.io/v1/game-api/pega/'
POSTGRES_URI = config("POSTGRES_URI")
PROXY_HOST = config("PROXY_HOST", default = None)
PROXY_PORT = config("PROXY_PORT", default = 3128, cast = int)

start_time = time.time()

def get_data_from_db():
    meta_data = MetaData()
    engine = create_engine(POSTGRES_URI)
    pegas_table = pegas_schema(meta_data)

    conn = engine.connect()

    Session = sessionmaker(bind=engine)

    session = Session()

    result = list(
        conn.execute(
            select(pegas_table.c.id).where(
                pegas_table.c.name == None).limit(DB_PAGE_SIZE)
        )
    )

    return session, pegas_table, list(itertools.chain.from_iterable(result))


@retry(retry_policy)
async def parse_from_api(pega_id, sql_session, pegas_table):
    pega_url = API_BASE_URL+str(pega_id)

    async with aiohttp.ClientSession() as session:
        await limiter.acquire()
        if (PROXY_HOST is not None):
            response = await session.get(url=pega_url, proxy = f"http://{PROXY_HOST}:{PROXY_PORT}")
        else:
            response = await session.get(url=pega_url)
        
        print(pega_url)
        
        if (response.status != 200):
            raise Exception(f"Response code: {response.status}")

        text = await response.read()
        
        if (text == "Too many requests, please try again later."):
            raise Exception(f"Response code: 429")
        
        data = json.loads(text.decode())
        
        pega_info = {
            'name': data['pega']['name'],
            'father_id': data['pega']['fatherId'],
            'mother_id': data['pega']['motherId'],
            'gender': data['pega']['gender'],
            'bloodline': data['pega']['bloodLine'],
            'avatar_id_1': data['pega']['design']['avatar'].split('/')[-1],
            'avatar_id_2': data['pega']['design']['avatar_2'].split('/')[-1]
        }

        sql_session.query(pegas_table).filter(
            pegas_table.c.id == pega_id).update(pega_info)
        sql_session.commit()

async def limited(until):
    duration = int(round(until - time.time()))
    print('Rate limited, sleeping for {:d} seconds'.format(duration))
    
async def gather_data():
    sql_session, pegas_table, list_of_ids = get_data_from_db()
    await asyncio.gather(*[parse_from_api(pega_id, sql_session, pegas_table) for pega_id in list_of_ids])
            


if __name__ == '__main__':
    # asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())  # Necessary for Windows users
    loop = asyncio.get_event_loop()
    loop.run_until_complete(gather_data())
    # asyncio.run(gather_data())
    end_time = time.time() - start_time
    print(f"\nExecution time: {end_time} seconds")
