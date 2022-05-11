import asyncio
import time

from db.pg_db import PgDb
from services.parse_pegas import parse_pegas

start_time = time.time()

if __name__ == '__main__':
    pg_db = PgDb()

    # asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())  # Necessary for Windows users
    loop = asyncio.get_event_loop()
    loop.run_until_complete(parse_pegas(pg_db))
    end_time = time.time() - start_time
    print(f"\nExecution time: {end_time} seconds")
