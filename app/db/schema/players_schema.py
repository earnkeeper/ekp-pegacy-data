from sqlalchemy import Column, DateTime, String, Table


def players_schema(meta_data):
    return Table('players', meta_data,
                 Column('id', String(64), primary_key=True),
                 Column('created', DateTime(), nullable=False),
                 Column('updated', DateTime(), nullable=False),
                 Column('address', String(42), nullable=False, unique=True),
                 # TODO check default value of nullable
                 Column('earned_to_date', String(64)),
                 Column('earned_to_date_coin_id', String(64)),
                 )
