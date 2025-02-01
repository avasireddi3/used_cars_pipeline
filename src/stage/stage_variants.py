import polars as pl


def find_missing_variants(listings_df: pl.DataFrame, variants_df: pl.DataFrame) -> list:
    """get missing variant ids from a listings dataframe"""
    missing_variants = (listings_df.join(
        other=variants_df,
        how="left",
        left_on="variant_id",
        right_on="variant_id",
        suffix="_1",
        coalesce=False
    ).filter(pl.col("variant_id_1").is_null()).
                        get_column("variant_id").
                        unique().
                        to_list())
    print(missing_variants)
    return missing_variants