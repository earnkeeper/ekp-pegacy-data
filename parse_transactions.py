import re
from datetime import datetime

from sqlalchemy import select
from sqlalchemy.dialects.postgresql import insert

PAGE_SIZE = 1000
# Market Contract
CONTRACT_ADDRESS = "0x66e4e493bab59250d46bfcf8ea73c02952655206"


def parse_transactions(collection, engine, conn, market_buys_table, players_table, pegas_table):

    latest_timestamp_from_market_buys = 0
    result = list(
        conn.execute(
            select(market_buys_table).order_by('created').limit(1)
        )
    )

    if (len(result) > 0):
        latest_timestamp_from_market_buys = int(
            result[0]["created"].timestamp())
        print(
            f'Latest timestamp from db is: {latest_timestamp_from_market_buys}')

    while (True):
        re.IGNORECASE
        next_trans = list(
            collection.find(
                {
                    "source_contract_address": CONTRACT_ADDRESS,
                    "input": {"$regex": re.compile("^0x0bb5eaf3")},
                    "timeStamp": {"$gt": latest_timestamp_from_market_buys}
                }
            )
            .sort("blockNumber", 1)
            .limit(PAGE_SIZE)
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

        conn.execute(
            insert(market_buys_table)
            .on_conflict_do_nothing(index_elements=["id"]),
            records
        )

        conn.execute(
            insert(players_table)
            .on_conflict_do_nothing(index_elements=["id"]),
            players
        )

        stmt = insert(pegas_table)

        conn.execute(
            stmt
            .on_conflict_do_update(
                index_elements=["id"],
                set_={
                    "cost": stmt.excluded.cost,
                    "owner_player_id": stmt.excluded.owner_player_id
                }
            ),
            pegas
        )

        print(f'Processed {len(next_trans)} market_buys...')

        if len(next_trans) < PAGE_SIZE:
            break
