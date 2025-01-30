import polars as pl


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

