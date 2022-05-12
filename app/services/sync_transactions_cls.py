# from db.pg_db import PgDb
from ...db.mongo_db import MongoDb
from decouple import config
import requests


class SyncTransactions:
    POLYGONSCAN_API_KEY = config('POLYGONSCAN_API_KEY')

    def __init__(self, contract_address, max_trans_to_fetch=0):
        self.contract_address = contract_address
        self.max_trans_to_fetch = max_trans_to_fetch
        self.mongo_db = MongoDb()
        self.start_block = 0
        self.page_size = 1000

        self.get_latest_start_block()

        self.write_main()

    def get_latest_start_block(self):
        latest = self.mongo_db.get_latest(contract_address=self.contract_address)
        if latest is not None and len(latest):
            self.start_block = latest[0]["blockNumber"]

    def get_trans(self):
        url = f'https://api.polygonscan.com/api?module=account&action=txlist&address={self.contract_address}&startblock={self.start_block}&page=1&offset={self.page_size}&sort=asc&apiKey={self.POLYGONSCAN_API_KEY}'

        response = requests.get(url)

        trans = response.json()["result"]

        return response, trans

    def write_main(self):
        while True:
            print(f"Retrieving trans from api starting at block {self.start_block}")
            response, trans = self.get_trans()
            if trans is None:
                print(response.json())

            if len(trans) == 0:
                break

            print(f"Retrieved {len(trans)} from the api, saving to db...")

            for tran in trans:
                block_number = int(tran["blockNumber"])

                if (block_number > self.start_block):
                    self.start_block = block_number

                tran["blockNumber"] = block_number
                tran["source_contract_address"] = self.contract_address
                tran["confirmations"] = int(tran["confirmations"])
                tran["cumulativeGasUsed"] = int(tran["cumulativeGasUsed"])
                tran["gas"] = int(tran["gas"])
                tran["gasUsed"] = int(tran["gasUsed"])
                tran["gasUsed"] = int(tran["gasUsed"])
                tran["isError"] = tran["isError"] == "1"
                tran["timeStamp"] = int(tran["timeStamp"])
                tran["transactionIndex"] = int(tran["transactionIndex"])

            self.mongo_db.bulk_write(trans)

            if (len(trans) < self.page_size or self.max_trans_to_fetch > 0 and len(trans) > self.max_trans_to_fetch):
                break
