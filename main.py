import polars as pl
import sqlalchemy.exc

from src.ingest import api_scraper
from src.ingest.api_scraper import generate_brands_dict, get_brand_cars, get_variant_info
from src.persist.stage import insert_listings, get_variants_db, insert_variants, get_missing_variants, get_listings_db, \
    insert_unsold_listings, insert_sold_listings, get_sold_db
from src.transform.transform_data import initialize_df_listings, string_operations_listings, initialize_df_variant, \
    find_unsold, find_sold


def main():
    listings_raw = api_scraper.get_listings()
    brands_dict = generate_brands_dict(listings_raw)

    #TODO: see if processing can be asyncronized

    # for brand in brands_dict:
    #     brand_cars = get_brand_cars(brand, brands_dict)

    brand_cars = get_brand_cars("bmw",brands_dict)
    listings_df = initialize_df_listings(brand_cars)
    listings_df_clean = string_operations_listings(listings_df)
    insert_listings(listings_df_clean)

    try:
        old_listings = get_listings_db()
    except sqlalchemy.exc.ProgrammingError:
        old_listings = pl.DataFrame()

    if old_listings.is_empty():
        unsold_ids = listings_df_clean.get_column("id").to_list()
        insert_unsold_listings(unsold_ids)
    else:
        unsold_ids = find_unsold(listings_df_clean,get_sold_db())
        sold_ids = find_sold(listings_df_clean,old_listings)
        insert_unsold_listings(unsold_ids)
        insert_sold_listings(sold_ids)

    try:
        variants_df = get_variants_db()
    except sqlalchemy.exc.ProgrammingError:
        variants_df = pl.DataFrame()

    if variants_df.is_empty():
        variant_ids = listings_df_clean.get_column("variant_id").to_list()
    else:
        variant_ids = get_missing_variants(listings_df)

    variants_data = get_variant_info(variant_ids)
    variants_df_insert = initialize_df_variant(variants_data)
    insert_variants(variants_df_insert)




if __name__ == "__main__":
    main()



