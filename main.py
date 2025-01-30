import polars as pl
import sqlalchemy.exc

from src.extract import extract_listings, extract_variants
from src.transform import transform_listings, transform_variants
from src.load import load_listings, load_variants, load_status
from src.stage import stage_status, stage_variants

def main():
    brands_mapping = extract_listings.brand_mapping()

    #TODO: see if processing can be asyncronized

    # for brand in brands_dict:
    #     brand_cars = get_brand_cars(brand, brands_dict)

    brand_listings = extract_listings.listings_data("bmw", brands_mapping)
    brand_listings_clean = transform_listings.full_transform(brand_listings)
    load_listings.insert_data(brand_listings_clean)

    try:
        old_listings = load_listings.read_data()
    except sqlalchemy.exc.ProgrammingError:
        old_listings = pl.DataFrame()

    if old_listings.is_empty():
        unsold_ids = load_listings.read_data().get_column("id").to_list()
        load_status.insert_unsold_data(unsold_ids)
    else:
        unsold_ids = stage_status.find_unsold(brand_listings_clean,
                                              load_status.read_sold())
        sold_ids = stage_status.find_sold(brand_listings_clean,old_listings)
        load_status.insert_sold_data(sold_ids)
        load_status.insert_unsold_data(unsold_ids)

    try:
        variants_df = load_variants.read_data()
    except sqlalchemy.exc.ProgrammingError:
        variants_df = pl.DataFrame()

    if variants_df.is_empty():
        variant_ids = brand_listings_clean.get_column("variant_id").to_list()
    else:
        variant_ids = stage_variants.find_missing_variants(brand_listings_clean,
                                                           variants_df)

    variants_data = extract_variants.variants_data(variant_ids)
    variants_df_insert = transform_variants.initialize_df(variants_data)
    load_variants.insert_data(variants_df_insert)




if __name__ == "__main__":
    main()



