from decouple import config
from pymongo import DESCENDING, MongoClient

MONGO_URI = config('MONGO_URI', default='mongodb://localhost:27017/')
MONGO_DB_NAME = config('MONGO_DB_NAME', default='pegaxy')


class MongoDb:
    def __init__(self):
        self.client = MongoClient(MONGO_URI)
        self.db = self.client[MONGO_DB_NAME]

        self.contract_transactions = self.db['contract_transactions']
        self.contract_transactions.create_index("hash", unique=True)
        self.contract_transactions.create_index([("blockNumber", DESCENDING)])
        self.contract_transactions.create_index([("timeStamp", DESCENDING)])
        self.contract_transactions.create_index("source_contract_address")
