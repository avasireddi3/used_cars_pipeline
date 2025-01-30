import datetime
import polars as pl
from sqlalchemy import create_engine


db_url = "postgresql+psycopg2://postgres:Niki2004$@localhost:5432/usedcars2"
engine = create_engine(db_url)


def read_sold() -> pl.DataFrame:
    """get the sold table as a dataframe"""
    with engine.connect() as conn:
        df = pl.read_database(connection=conn, query="SELECT * FROM sold_status_demo")
    return df


def insert_sold_data(sold_ids:list)->None:
    data = [
        pl.Series("id",sold_ids),
        pl.Series("status",["sold"]*len(sold_ids)),
        pl.Series("timestamp", [datetime.datetime.now()]*len(sold_ids))
    ]
    insert_df = pl.DataFrame(data)
    with engine.connect() as conn:
        insert_df.write_database(
            table_name='sold_status_demo',
            connection=conn,
            if_table_exists='append'
        )

def insert_unsold_data(unsold_ids:list)->None:
    data = [
        pl.Series("id", unsold_ids),
        pl.Series("status", ["unsold"] * len(unsold_ids)),
        pl.Series("timestamp", [datetime.datetime.now()] * len(unsold_ids))
    ]
    insert_df = pl.DataFrame(data)
    with engine.connect() as conn:
        insert_df.write_database(
            table_name='sold_status_demo',
            connection=conn,
            if_table_exists='append'
        )