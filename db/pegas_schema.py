from sqlalchemy import (BigInteger, Column, Date, DateTime, Float, ForeignKey,
                        Integer, MetaData, String, Table, Text, create_engine)

def pegas_schema(meta_data):
    return Table('pegas', meta_data,
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