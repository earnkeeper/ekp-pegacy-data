from decouple import config
from pymongo import DESCENDING, MongoClient

from db.init_db import init_pg_db
from parse_transactions import parse_transactions
from sync_transactions import sync_transactions

init_pg_db()

MONGO_URL = config('MONGO_URL', default='mongodb://localhost:27017/')

def init_mongo_db():
    client = MongoClient(MONGO_URL)
    return client['pegaxy']


def init_contract_transactions_collection(db):
    collection = db['contract_transactions']
    collection.create_index("hash", unique=True)
    collection.create_index([("blockNumber", DESCENDING)])
    collection.create_index([("timeStamp", DESCENDING)])
    collection.create_index("source_contract_address")
    return collection


mongo_db = init_mongo_db()
collection = init_contract_transactions_collection(mongo_db)

# Pegaxy Market
# sync_transactions('0x66e4e493bab59250d46bfcf8ea73c02952655206', collection)
# PGX token
# sync_transactions('0xc1c93D475dc82Fe72DBC7074d55f5a734F8cEEAE', collection)

# parse_transactions(collection)
