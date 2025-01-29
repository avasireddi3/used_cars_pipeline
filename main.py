import polars as pl
import sqlalchemy.exc

from src.ingest import api_scraper
from src.ingest.api_scraper import generate_brands_dict, get_brand_cars, get_variant_info
from src.persist.stage import insert_listings, get_variants_db, insert_variants, get_missing_variants
from src.transform.transform_data import initialize_df_listings, string_operations_listings, initialize_df_variant


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

    print(get_variants_db().head())



if __name__ == "__main__":
    main()



