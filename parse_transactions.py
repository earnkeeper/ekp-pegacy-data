import re
from datetime import datetime

from sqlalchemy.dialects.postgresql import insert


def parse_transactions(collection, conn, market_buys_table):
    # Market Contract
    contract_address = "0x66e4e493bab59250d46bfcf8ea73c02952655206"
    re.IGNORECASE
    next_trans = list(
        collection.find(
            {
                "source_contract_address": contract_address,
                "input": {"$regex": re.compile("^0x0bb5eaf3")}
            }
        )
        .sort("blockNumber", 1)
        .limit(100)
    )

    records = []

    for next_tran in next_trans:
        price = str(int(next_tran["input"][74:138], 16))
        token_id = int(next_tran["input"][138:202], 16)

        record = {
            "id": next_tran["hash"],
            "created": datetime.fromtimestamp(next_tran["timeStamp"]),
            "updated": datetime.now(),
            "buyer_address": next_tran["from"],
            "price": price,
            "price_coin_id": "tether",
            "pega_token_id": token_id
        }
        records.append(record)

    conn.execute(
        insert(market_buys_table)
        .on_conflict_do_nothing(index_elements=["id"]),
        records
    )
