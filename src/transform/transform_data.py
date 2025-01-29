import polars as pl


def initialize_df_listings(data: list) -> pl.DataFrame:
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


def string_operations_listings(df: pl.DataFrame) -> pl.DataFrame:
    result = df.with_columns(pl.col("mileage").str.replace_all(",", "").cast(pl.Int32))
    return result


def initialize_df_variant(data: list) -> pl.DataFrame:
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


def string_operations_variants(df: pl.DataFrame) -> pl.DataFrame:
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

def find_sold(new_listings:pl.DataFrame,old_listings:pl.DataFrame)->list:
    """find sold listing ids since last update"""
    sold_ids = (old_listings.join(
        other = new_listings,
        left_on="id",
        right_on="id",
        suffix="_1",
        how="left").
        select("id","id_1").
        filter(pl.col("id_1").is_null()).
        get_column("id").
        to_list())
    return sold_ids

def find_unsold(new_listings:pl.DataFrame,sold_status:pl.DataFrame)->list:
    unique_ids = sold_status.get_column("id").unique()
    sold_ids = pl.DataFrame(unique_ids)
    unsold_ids = (new_listings.join(
        other=sold_ids,
        left_on="id",
        right_on="id",
        how="left",
        suffix="_1").
        filter(pl.col("id_1").is_null()).
        get_column("id").
        to_list())
    return unsold_ids