import asyncio

from decouple import config

from db.mongo_db import MongoDb
from db.pg_db import PgDb
from services.parse_transactions import parse_transactions
from services.sync_transactions import sync_transactions

if __name__ == '__main__':
    pg_db = PgDb()
    mongo_db = MongoDb()

    loop = asyncio.get_event_loop()

    # Pegaxy Market
    loop.run_until_complete(
        sync_transactions(
            '0x66e4e493bab59250d46bfcf8ea73c02952655206',
            mongo_db,
            config("MAX_TRANS_TO_FETCH", default=0, cast=int)
        )
    )

    # PGX token
    # sync_transactions('0xc1c93D475dc82Fe72DBC7074d55f5a734F8cEEAE', mongo_db)

    parse_transactions(mongo_db, pg_db)
