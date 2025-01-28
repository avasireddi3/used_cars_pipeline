import polars as pl

def initialize_df_listings(data:list)->pl.DataFrame:
    df = pl.DataFrame(
        data,
        schema={'id':pl.Int32,
                'variant_id':pl.Int32,
                'body_type':pl.String,
                'city':pl.String,
                'price':pl.String,
                'fuel_type':pl.String,
                'mileage':pl.String,
                'make':pl.String,
                'model':pl.String,
                'gear':pl.String,
                'owner':pl.String},
        orient="row"
    )
    return df

def string_operations_listings(df:pl.DataFrame)->pl.DataFrame:
    result = df.with_columns(
        pl.col("mileage").str.replace_all(",","").cast(pl.Int32)
    )
    return result