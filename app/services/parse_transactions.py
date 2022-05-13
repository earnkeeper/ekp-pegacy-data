import re
from datetime import datetime

class ParseTransactions:

    def __init__(self, mongo_db, pg_db, contract_address):
        self.pg_db = pg_db
        self.mongo_db = mongo_db
        self.contract_address = contract_address
        self.page_size = 1000
        self.latest_timestamp_from_market_buys = 0

    def get_latest_timestamp_from_market_buys(self):
        result = self.pg_db.get_latest()
        if (len(result) > 0):
            self.latest_timestamp_from_market_buys = int(
                result[0]["created"].timestamp())
            print(
                f'Latest timestamp from db is: {self.latest_timestamp_from_market_buys}')

    def process(self):
        self.get_latest_timestamp_from_market_buys()
        
        while True:
            re.IGNORECASE
            next_trans = self.mongo_db.get_next_trans(
                contract_address=self.contract_address,
                latest_timestamp_from_market_buys=self.latest_timestamp_from_market_buys,
                pagesize=self.page_size,
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

                if timestamp > self.latest_timestamp_from_market_buys:
                    self.latest_timestamp_from_market_buys = timestamp

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

            self.pg_db.insert_to_market_buys_table(data=records)

            self.pg_db.insert_to_players_table(data=players)

            self.pg_db.insert_to_pegas_table(data=pegas)

            print(f'Processed {len(next_trans)} market_buys...')

            if len(next_trans) < self.page_size:
                break

