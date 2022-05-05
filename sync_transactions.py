import requests
from decouple import config
from pymongo import MongoClient, UpdateOne, DESCENDING

POLYGONSCAN_API_KEY = config('POLYGONSCAN_API_KEY')
MONGO_URL = config('MONGO_URL', default='mongodb://localhost:27017/')

client = MongoClient(MONGO_URL)
db = client['pegaxy']
collection = db['contract_transactions']
collection.create_index("hash", unique=True)
collection.create_index([("blockNumber", DESCENDING)])
collection.create_index([("timeStamp", DESCENDING)])
collection.create_index("source_contract_address")

def sync_transactions(contract_address):
    start_block = 0
    page_size = 5000

    latest = list(collection.find({ "source_contract_address": contract_address }).sort("blockNumber", -1).limit(1))

    if latest is not None and len(latest):
        start_block = latest[0]["blockNumber"]

    while (True):
        print(f"Retrieving trans from api starting at block {start_block}")
        url = f'https://api.polygonscan.com/api?module=account&action=txlist&address={contract_address}&startblock={start_block}&page=1&offset={page_size}&sort=asc&apiKey={POLYGONSCAN_API_KEY}'

        response = requests.get(url)

        trans = response.json()["result"]

        if (trans is None):
            print(response.json())

        if (len(trans) == 0):
            break

        print(f"Retrieved {len(trans)} from the api, saving to db...")

        for tran in trans:
            block_number = int(tran["blockNumber"])

            if (block_number > start_block):
                start_block = block_number

            tran["blockNumber"] = block_number
            tran["source_contract_address"] = contract_address
            tran["confirmations"] = int(tran["confirmations"])
            tran["cumulativeGasUsed"] = int(tran["cumulativeGasUsed"])
            tran["gas"] = int(tran["gas"])
            tran["gasUsed"] = int(tran["gasUsed"])
            tran["gasUsed"] = int(tran["gasUsed"])
            tran["isError"] = tran["isError"] == "1"
            tran["timeStamp"] = int(tran["timeStamp"])
            tran["transactionIndex"] = int(tran["transactionIndex"])


        def format_write(tran):
            return UpdateOne({ "hash": tran["hash"] }, { "$set": tran }, True);

        collection.bulk_write(
            list(map(lambda tran: format_write(tran), trans ))
        )

        if (len(trans) < page_size):
            break

