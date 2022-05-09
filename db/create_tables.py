from sqlalchemy import (create_engine, Float, Text, MetaData,

                        Table, Column, Integer, String, DateTime,

                        Date, BigInteger, ForeignKey)

from datetime import datetime

meta_data = MetaData()

DATABASE_URI = 'postgresql+psycopg2://postgres:pythonista0505@localhost:5432/pegaxy'


players = Table('players', meta_data,
      Column('id', Integer(), primary_key=True),
      Column('created', DateTime(), nullable=False),
      Column('updated', DateTime(), nullable=False),
      Column('address', String(42), nullable=False, unique=True),
      Column('earned_to_date', BigInteger()),  # TODO check default value of nullable
)

market_buy = Table('market_buys', meta_data,
                   Column('id', Integer(), primary_key=True),
                   Column('created', DateTime(), nullable=False),
                   Column('updated', DateTime(), nullable=False),
                   Column('buyer_address', ForeignKey('players.address'), nullable=False),
                   Column('price', BigInteger(), nullable=False),
                   Column('price_token_id', String(64), nullable=False),
                   Column('pega_token_id', String(64), nullable=False),
                   )

pega = Table('pegas', meta_data,
             Column('id', Integer(), primary_key=True),
             Column('created', DateTime(), nullable=False),
             Column('updated', DateTime(), nullable=False),
             Column('name', String(150), nullable=False),
             Column('cost', BigInteger()),
             Column('market_value', BigInteger()),
             Column('earned_to_date', BigInteger()),
             Column('place_rate', Float()),
             Column('total_races', Integer()),
             Column('owner_player_id', ForeignKey('players.id'), nullable=False),
             )

engine = create_engine(DATABASE_URI)

try:
    conn = engine.connect()
    print('db connected')
    print('connection object is :{}'.format(conn))

except:
    print('db not connected')

meta_data.create_all(engine)
