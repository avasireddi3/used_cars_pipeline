import psycopg2
import polars as pl
from sqlalchemy import create_engine

db_url = "postgresql+psycopg2://postgres:Niki2004$@localhost:5432/usedcars2"
engine = create_engine(db_url)

def insert_listings(listings_df:pl.DataFrame)->None:
    with engine.connect() as conn:
        listings_df.write_database(
            table_name="listings_demo_2",
            connection=conn,
            if_table_exists='replace'
        )
        df = pl.read_database(
            connection=conn,
            query="SELECT * FROM listings_demo_2 LIMIT 5"
        )
    print(df.head())