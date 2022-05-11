import requests
from decouple import config
from pymongo import DESCENDING, MongoClient, UpdateOne

POLYGONSCAN_API_KEY = config('POLYGONSCAN_API_KEY')


def sync_transactions(contract_address, mongo_db, max_trans_to_fetch=0):
    start_block = 0
    page_size = 1000

    latest = list(mongo_db.contract_transactions.find(
        {"source_contract_address": contract_address}).sort("blockNumber", -1).limit(1))

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
            return UpdateOne({"hash": tran["hash"]}, {"$set": tran}, True)

        mongo_db.contract_transactions.bulk_write(
            list(map(lambda tran: format_write(tran), trans))
        )

        if (len(trans) < page_size or max_trans_to_fetch > 0 and len(trans) > max_trans_to_fetch):
            break
