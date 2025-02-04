import polars as pl
from airflow.decorators import task
from sqlalchemy import create_engine



def initialize_df(data: list) -> pl.DataFrame:
    df = pl.DataFrame(
        data,
        schema={
            "id": pl.Int32,
            "variant_id": pl.Int32,
            "body_type": pl.String,
            "city": pl.String,
            "price": pl.String,
            "fuel_type": pl.String,
            "mileage": pl.String,
            "make": pl.String,
            "model": pl.String,
            "gear": pl.String,
            "owner": pl.String,
        },
        orient="row",
    )
    return df


@task
def full_transform(data:list)->tuple[int,int]:
    db_url = "postgresql+psycopg2://airflow:airflow@postgres/airflow"
    engine = create_engine(db_url)
    df = initialize_df(data)
    df_final = df.with_columns(pl.col("mileage").str.replace_all(",", "").cast(pl.Int32))
    with engine.connect() as conn:
        df_final.write_database(
            table_name="listings_demo_2", connection=conn, if_table_exists="replace"
        )
    return df_final.shape