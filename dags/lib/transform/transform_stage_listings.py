import polars as pl
from airflow.decorators import task



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
def transform_stage_listings(passed:tuple[str,int])->tuple[int,int]:
    brand=passed[0]
    data=pl.read_csv(f"/sources/tmp/listings/{brand}_stage_1.csv")
    df = initialize_df(data)
    df_final = df.with_columns(pl.col("mileage").str.replace_all(",", "").cast(pl.Int32))
    df_final.write_csv(f"/sources/tmp/listings/{brand}_stage_2.csv",)
    return df_final.shape

def main():
    return NotImplemented

if __name__=="__main__":
    main()