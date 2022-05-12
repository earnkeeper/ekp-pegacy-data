import re
from datetime import datetime

from sqlalchemy import select
from sqlalchemy.dialects.postgresql import insert

PAGE_SIZE = 1000
# Market Contract
CONTRACT_ADDRESS = "0x66e4e493bab59250d46bfcf8ea73c02952655206"


def parse_transactions(mongo_db, pg_db):

    latest_timestamp_from_market_buys = 0
    result = pg_db.get_latest()

    if (len(result) > 0):
        latest_timestamp_from_market_buys = int(
            result[0]["created"].timestamp())
        print(
            f'Latest timestamp from db is: {latest_timestamp_from_market_buys}')

    while (True):
        re.IGNORECASE
        next_trans = mongo_db.get_next_trans(
            contract_address=CONTRACT_ADDRESS,
            latest_timestamp_from_market_buys=latest_timestamp_from_market_buys,
            pagesize=PAGE_SIZE,
            start_string="^0x0bb5eaf3"
        )

        if len(next_trans) == 0:
            print('No more raw market buys to process')
            break

        records = []
        players = []
        pegas = []

        for next_tran in next_trans:
            price = str(int(next_tran["input"][74:138], 16))
            token_id = int(next_tran["input"][138:202], 16)
            timestamp = next_tran["timeStamp"]
            player_id = next_tran["from"]

            if timestamp > latest_timestamp_from_market_buys:
                latest_timestamp_from_market_buys = timestamp

            record = {
                "id": next_tran["hash"],
                "created": datetime.fromtimestamp(next_tran["timeStamp"]),
                "updated": datetime.now(),
                "buyer_address": player_id,
                "price": price,
                "price_coin_id": "tether",
                "pega_token_id": token_id
            }

            player = {
                "id": player_id,
                "created": datetime.fromtimestamp(next_tran["timeStamp"]),
                "updated": datetime.now(),
                "address": player_id,
            }

            pega = {
                "id": token_id,
                "created": datetime.fromtimestamp(next_tran["timeStamp"]),
                "updated": datetime.now(),
                "cost": price,
                "owner_player_id": player_id
            }

            records.append(record)
            players.append(player)
            pegas.append(pega)

        pg_db.insert_to_market_buys_table(data=records)

        pg_db.insert_to_players_table(data=players)

        pg_db.insert_to_pegas_table(data=pegas)

        print(f'Processed {len(next_trans)} market_buys...')

        if len(next_trans) < PAGE_SIZE:
            break
