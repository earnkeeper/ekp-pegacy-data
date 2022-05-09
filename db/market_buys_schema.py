from sqlalchemy import Column, DateTime, String, Table


def market_buys_schema(meta_data):
    return Table('market_buys', meta_data,
                 Column('id', String(64), primary_key=True),
                 Column('created', DateTime(), nullable=False),
                 Column('updated', DateTime(), nullable=False),
                 Column('buyer_address', String(64), nullable=False),
                 Column('price', String(64), nullable=False),
                 Column('price_coin_id', String(64), nullable=False),
                 Column('pega_token_id', String(64), nullable=False),
                 )
