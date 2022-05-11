import asyncio
import itertools
import json
import time

import aiohttp
from aiolimiter import AsyncLimiter
from aioretry import retry
from decouple import config
from sqlalchemy import select

from sdk.retry import defaullt_retry_policy

PROXY_HOST = config("PROXY_HOST", default=None)
PROXY_PORT = config("PROXY_PORT", default=3128, cast=int)

HTTP_REQ_PER_SEC = 30
DB_PAGE_SIZE = 50
API_BASE_URL = 'https://api-apollo.pegaxy.io/v1/game-api/pega/'
limiter = AsyncLimiter(HTTP_REQ_PER_SEC, time_period=1)

def get_data_from_db(pg_db):
    result = list(
        pg_db.conn.execute(
            select(pg_db.pegas.c.id).where(
                pg_db.pegas.c.name == None).limit(DB_PAGE_SIZE)
        )
    )

    return list(itertools.chain.from_iterable(result))

@retry(defaullt_retry_policy)
async def parse_from_api(pega_id, pg_db):
    pega_url = API_BASE_URL+str(pega_id)

    async with aiohttp.ClientSession() as session:

        await limiter.acquire()

        print(pega_url)

        if (PROXY_HOST is not None):
            response = await session.get(url=pega_url, proxy=f"http://{PROXY_HOST}:{PROXY_PORT}")
        else:
            response = await session.get(url=pega_url)

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

        print(f"Updating pega id {pega_id} in the database")

        pg_db.session.query(pg_db.pegas).filter(
            pg_db.pegas.c.id == pega_id
        ).update(pega_info)

        pg_db.session.commit()


async def limited(until):
    duration = int(round(until - time.time()))
    print('Rate limited, sleeping for {:d} seconds'.format(duration))


async def parse_pegas(pg_db):
    while True:
        print(f"Fetching new pega ids from database")

        list_of_ids = get_data_from_db(pg_db)

        print(f"Processing {len(list_of_ids)} pega ids")

        if not list_of_ids:
            break

        await asyncio.gather(*[parse_from_api(pega_id, pg_db) for pega_id in list_of_ids])
