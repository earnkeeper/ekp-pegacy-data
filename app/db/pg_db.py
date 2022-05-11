from decouple import config
from sqlalchemy import MetaData, create_engine
from sqlalchemy.orm import sessionmaker

from db.schema.market_buys_schema import market_buys_schema
from db.schema.pegas_schema import pegas_schema
from db.schema.players_schema import players_schema

POSTGRES_URI = config("POSTGRES_URI")

class PgDb:
    def __init__(self):
        self.meta_data = MetaData()

        self.engine = create_engine(POSTGRES_URI)
        self.players = players_schema(self.meta_data)
        self.market_buys = market_buys_schema(self.meta_data)
        self.pegas = pegas_schema(self.meta_data)

        try:
            self.conn = self.engine.connect()
            print('db connected')
            print('connection object is :{}'.format(self.conn))

        except:
            print('db not connected')

        Session = sessionmaker(bind=self.engine)
        self.session = Session()
        self.meta_data.create_all(self.engine)        