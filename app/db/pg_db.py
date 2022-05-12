import itertools

from decouple import config
from sqlalchemy import MetaData, create_engine
from sqlalchemy.orm import sessionmaker

from db.schema.market_buys_schema import market_buys_schema
from db.schema.pegas_schema import pegas_schema
from db.schema.players_schema import players_schema
from sqlalchemy import select
from sqlalchemy.dialects.postgresql import insert

POSTGRES_URI = config("POSTGRES_URI")


class PgDb:
    def __init__(self):
        self.meta_data = MetaData()
        print('connecting to postgres')

        self.engine = create_engine(POSTGRES_URI)
        self.players = players_schema(self.meta_data)
        self.market_buys = market_buys_schema(self.meta_data)
        self.pegas = pegas_schema(self.meta_data)

        self.conn = self.engine.connect()
        print('postgres db connected')

        Session = sessionmaker(bind=self.engine)
        self.session = Session()
        self.meta_data.create_all(self.engine)

    def get_latest(self):
        return list(
            self.conn.execute(
                select(self.market_buys).order_by('created').limit(1)
            )
        )

    def get_rows_with_null(self, limit_page_size):
        rows = list(
                    self.conn.execute(
                        select(self.pegas.c.id).where(
                            self.pegas.c.name == None).
                            limit(limit_page_size)
                    )
                )
        return list(itertools.chain.from_iterable(rows))

    def insert_to_market_buys_table(self, data):
        self.conn.execute(
            insert(self.market_buys)
                .on_conflict_do_nothing(index_elements=["id"]),
            data
        )

    def insert_to_players_table(self, data):
        self.conn.execute(
            insert(self.market_buys)
                .on_conflict_do_nothing(index_elements=["id"]),
            data
        )

    def insert_to_pegas_table(self, data):
        stmt = insert(self.pegas)
        self.conn.execute(
            stmt.on_conflict_do_update(
                index_elements=["id"],
                set_={
                    "cost": stmt.excluded.cost,
                    "owner_player_id": stmt.excluded.owner_player_id
                }
            ),
            data
        )

    def update_query(self, pega_id, pega_info):
        self.session.query(self.pegas).filter(
            self.pegas.c.id == pega_id
        ).update(pega_info)

        self.session.commit()
