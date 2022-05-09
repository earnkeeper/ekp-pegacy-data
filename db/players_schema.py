from sqlalchemy import (BigInteger, Column, Date, DateTime, Float, ForeignKey,
                        Integer, MetaData, String, Table, Text, create_engine)

def players_schema(meta_data):
    return Table('players', meta_data,
                 Column('id', Integer(), primary_key=True),
                 Column('created', DateTime(), nullable=False),
                 Column('updated', DateTime(), nullable=False),
                 Column('address', String(42), nullable=False, unique=True),
                 # TODO check default value of nullable
                 Column('earned_to_date', BigInteger()),
                 )
