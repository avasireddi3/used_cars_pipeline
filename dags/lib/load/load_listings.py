import polars as pl
from sqlalchemy import create_engine
from airflow.decorators import task


db_url = "postgresql+psycopg2://airflow:airflow@postgres/usedcars2"
engine = create_engine(db_url)

@task
def load_listings() -> None:
    """insert a dataframe into the listings table"""
    listings_df = pl.scan_csv("/sources/tmp/listings/*_stage_2.csv").collect()
    with engine.connect() as conn:
        listings_df.write_database(
            table_name="listings_staging", connection=conn, if_table_exists="replace"
        )



