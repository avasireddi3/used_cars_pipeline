import datetime
import polars as pl
from sqlalchemy import create_engine

db_url = "postgresql+psycopg2://postgres:Niki2004$@localhost:5432/usedcars2"
engine = create_engine(db_url)

def read_data() -> pl.DataFrame:
    """get the listings table as a database"""
    with engine.connect() as conn:
        df = pl.read_database(connection=conn, query="SELECT * FROM listings_demo_2")
    return df

def insert_data(listings_df: pl.DataFrame) -> None:
    """insert a dataframe into the listings table"""
    with engine.connect() as conn:
        listings_df.write_database(
            table_name="listings_demo_2", connection=conn, if_table_exists="replace"
        )



