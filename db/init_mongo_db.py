from decouple import config
from pymongo import DESCENDING, MongoClient

MONGO_URL = config('MONGO_URL', default='mongodb://localhost:27017/')
MONGO_DB_NAME = config('MONGO_DB_NAME', default='pegaxy')


def init_mongo_db():
    client = MongoClient(MONGO_URL)
    db = client[MONGO_DB_NAME]
    collection = db['contract_transactions']
    collection.create_index("hash", unique=True)
    collection.create_index([("blockNumber", DESCENDING)])
    collection.create_index([("timeStamp", DESCENDING)])
    collection.create_index("source_contract_address")
    return [db, collection]
