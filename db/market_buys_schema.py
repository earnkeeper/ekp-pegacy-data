from sqlalchemy import (BigInteger, Column, Date, DateTime, Float, ForeignKey,
                        Integer, MetaData, String, Table, Text, create_engine)

def market_buys_schema(meta_data):
    return Table('market_buys', meta_data,
                 Column('id', Integer(), primary_key=True),
                 Column('created', DateTime(), nullable=False),
                 Column('updated', DateTime(), nullable=False),
                 Column('buyer_address', ForeignKey(
                     'players.address'), nullable=False),
                 Column('price', BigInteger(), nullable=False),
                 Column('price_token_id', String(64), nullable=False),
                 Column('pega_token_id', String(64), nullable=False),
                 )
