import datetime
import polars as pl
from sqlalchemy import create_engine


db_url = "postgresql+psycopg2://postgres:Niki2004$@localhost:5432/usedcars2"
engine = create_engine(db_url)


def read_data() -> pl.DataFrame:
    """get the variants table as a dataframe"""
    with engine.connect() as conn:
        df = pl.read_database(connection=conn, query="SELECT * FROM variants_demo_2")
    return df


def insert_data(variants_df: pl.DataFrame) -> None:
    """insert a variants df into the variants table"""
    with engine.connect() as conn:
        variants_df.write_database(
            table_name="variants_demo_2", connection=conn, if_table_exists="replace"
        )