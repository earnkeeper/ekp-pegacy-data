from decouple import config

from db.init_mongo_db import init_mongo_db
from db.init_pg_db import init_pg_db
from parse_transactions import parse_transactions
from sync_transactions import sync_transactions

[pg_conn, market_buys_table, players_table, pegas_table] = init_pg_db()
[mongo_db, contract_collection] = init_mongo_db()

# Pegaxy Market
sync_transactions(
    '0x66e4e493bab59250d46bfcf8ea73c02952655206',
    contract_collection,
    config("MAX_TRANS_TO_FETCH", default=0, cast=int)
)

# PGX token
# sync_transactions('0xc1c93D475dc82Fe72DBC7074d55f5a734F8cEEAE', collection)

parse_transactions(contract_collection, pg_conn, market_buys_table)
