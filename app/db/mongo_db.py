import re

from decouple import config
from pymongo import DESCENDING, MongoClient, UpdateOne

MONGO_URI = config('MONGO_URI', default='mongodb://localhost:27017/')
MONGO_DB_NAME = config('MONGO_DB_NAME', default='pegaxy')


class MongoDb:
    def __init__(self):
        print('connecting to mongodb')
        self.client = MongoClient(MONGO_URI)
        self.db = self.client[MONGO_DB_NAME]

        self.contract_transactions = self.db['contract_transactions']
        self.contract_transactions.create_index("hash", unique=True)
        self.contract_transactions.create_index([("blockNumber", DESCENDING)])
        self.contract_transactions.create_index([("timeStamp", DESCENDING)])
        self.contract_transactions.create_index("source_contract_address")
        print('connected to mongodb')

    def get_latest(self, contract_address):
        return list(
            self.contract_transactions.find(
                {"source_contract_address": contract_address}
            )
            .sort("blockNumber", -1).limit(1)
        )

    def get_next_trans(self, contract_address, latest_timestamp_from_market_buys, pagesize, start_string="^0x0bb5eaf3"):
        return list(
            self.contract_transactions.find(
                {
                    "source_contract_address": contract_address,
                    "input": {"$regex": re.compile(start_string)},
                    "timeStamp": {"$gt": latest_timestamp_from_market_buys}
                }
            )
            .sort("blockNumber", 1)
            .limit(pagesize)
        )

    @staticmethod
    def format_write(tran):
        return UpdateOne({"hash": tran["hash"]}, {"$set": tran}, True)

    def bulk_write(self, trans):
        self.contract_transactions.bulk_write(
            list(map(lambda tran: MongoDb.format_write(tran), trans))
        )
