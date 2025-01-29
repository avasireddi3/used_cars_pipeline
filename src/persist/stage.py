import polars as pl
from sqlalchemy import create_engine


db_url = "postgresql+psycopg2://postgres:Niki2004$@localhost:5432/usedcars2"
engine = create_engine(db_url)


def insert_listings(listings_df: pl.DataFrame) -> None:
    """insert a dataframe into the listings table"""
    with engine.connect() as conn:
        listings_df.write_database(
            table_name="listings_demo_2", connection=conn, if_table_exists="replace"
        )


def get_listings_db() -> pl.DataFrame:
    """get the listings table as a database"""
    with engine.connect() as conn:
        df = pl.read_database(connection=conn, query="SELECT * FROM listings_demo_2")
    return df


def insert_variants(variants_df: pl.DataFrame) -> None:
    """insert a variants df into the variants table"""
    with engine.connect() as conn:
        variants_df.write_database(
            table_name="variants_demo_2", connection=conn, if_table_exists="replace"
        )


def get_variants_db() -> pl.DataFrame:
    """get the variants table as a dataframe"""
    with engine.connect() as conn:
        df = pl.read_database(connection=conn, query="SELECT * FROM variants_demo_2")
    return df


def get_missing_variants(listings_df: pl.DataFrame) -> list:
    """get missing variant ids from a listings dataframe"""
    variants_df = get_variants_db()
    missing_variants = listings_df.join(
        other=variants_df,
        how="left",
        left_on="variant_id",
        right_on="variant_id",
        suffix="_1",
    ).filter(pl.col("variant_id_1").is_null())
    return missing_variants.get_column("variant_id").to_list()
