import polars as pl


def initialize_df(data: list) -> pl.DataFrame:
    df = pl.DataFrame(
        data,
        schema={
            "variant_id": pl.Int32,
            "engine_cc": pl.String,
            "ground_clearance_mm": pl.String,
            "mileage_kmpl": pl.String,
            "drive_type": pl.String,
            "seating_capacity": pl.String,
            "power": pl.String,
            "cylinders": pl.String,
            "gearbox": pl.String,
            "top_speed_kmph": pl.String,
            "enc": pl.String,
            "length_mm": pl.String,
            "width_mm": pl.String,
            "height_mm": pl.String,
        },
        orient="row",
    )
    return df

def string_operations(df: pl.DataFrame) -> pl.DataFrame:
    return df.with_columns(
        pl.col("engine_cc").str.replace_all(r"\D", "").cast(pl.Int16),
        pl.col("ground_clearance_mm").str.replace_all(" mm", "").cast(pl.Int16),
        pl.col("seating_capacity").cast(pl.Int8),
        pl.col("mileage_kmpl").str.replace_all(" kmpl", "").cast(pl.Int16),
        pl.col("power").str.replace_all(" bhp", "").cast(pl.Float32),
        pl.col("top_speed_kmph").str.replace_all(r"\D", "").cast(pl.Int16),
        pl.col("length_mm").str.replace_all(" mm", "").cast(pl.Int16),
        pl.col("width_mm").str.replace_all(" mm", "").cast(pl.Int16),
        pl.col("height_mm").str.replace_all(" mm", "").cast(pl.Int16),
    )

def full_transform(data:list)->pl.DataFrame:
    df = initialize_df(data)
    df_final = string_operations(df)
    return df_final