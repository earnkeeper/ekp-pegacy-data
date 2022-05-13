import asyncio
import time
from services.parse_pegas import ParsePegas
from db.pg_db import PgDb

start_time = time.time()

if __name__ == '__main__':
    pg_db = PgDb()

    parse_pegas = ParsePegas(pg_db=pg_db)
    # asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())  # Necessary for Windows users
    loop = asyncio.get_event_loop()
    loop.run_until_complete(parse_pegas.process())
    end_time = time.time() - start_time
    print(f"\nExecution time: {end_time} seconds")
