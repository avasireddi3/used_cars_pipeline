import polars as pl
from pathlib import Path
from airflow.decorators import task
from airflow.operators.python import get_current_context



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
def full_transform(passed:tuple[str,list[tuple]])->tuple[int,int]:
    brand=passed[0]
    data=passed[1]
    df = initialize_df(data)
    df_final = df.with_columns(pl.col("mileage").str.replace_all(",", "").cast(pl.Int32))
    df_final.write_csv(f"/sources/tmp/{brand}.csv",)
    return df_final.shape

def main():
    return NotImplemented

if __name__=="__main__":
    main()