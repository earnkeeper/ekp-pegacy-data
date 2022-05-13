from sqlalchemy import Column, DateTime, Float, Integer, String, Table


def pegas_schema(meta_data):
    return Table('pegas', meta_data,
                 Column('id', Integer(), primary_key=True),
                 Column('created', DateTime(), nullable=False),
                 Column('updated', DateTime(), nullable=False),
                 Column('avatar_id_1', String(64)),
                 Column('avatar_id_2', String(64)),
                 Column('bloodline', String(64)),
                 Column('breed_type', String(64)),
                 Column('class', Integer()),
                 Column('cost', String(64)),
                 Column('cost_coin_id', String(64)),
                 Column('earned_to_date', String(64)),
                 Column('earned_to_date_coin_id', String(64)),
                 Column('father_id', Integer()),
                 Column('gender', String(64)),
                 Column('market_value', String(64)),
                 Column('market_value_coin_id', String(64)),
                 Column('mother_id', Integer()),
                 Column('name', String(150)),
                 Column('owner_player_id', String(64), nullable=False),
                 Column('place_rate', Float()),
                 Column('total_races', Integer()),
                 )
