import asyncio

from decouple import config
from db.mongo_db import MongoDb
from db.pg_db import PgDb

from services.sync_transactions import SyncTransactions
from services.parse_transactions import ParseTransactions

MARKET_CONTRACT_ADDRESS = '0x66e4e493bab59250d46bfcf8ea73c02952655206'

if __name__ == '__main__':
    pg_db = PgDb()
    mongo_db = MongoDb()

    loop = asyncio.get_event_loop()

    market_sync = SyncTransactions(
        MARKET_CONTRACT_ADDRESS,
        mongo_db,
        config("MAX_TRANS_TO_FETCH", default=0, cast=int)
    )
    
    # Pegaxy Market
    loop.run_until_complete(
        market_sync.process()
    )

    # PGX token
    # sync_transactions('0xc1c93D475dc82Fe72DBC7074d55f5a734F8cEEAE', mongo_db)

    parse_transactions = ParseTransactions(mongo_db, pg_db, MARKET_CONTRACT_ADDRESS)
    parse_transactions.process()
    