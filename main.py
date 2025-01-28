import json
from src.ingest import api_scraper
from src.ingest.api_scraper import generate_brands_dict, get_brand_cars
from src.persist import load
from src.persist.load import check_variant_exists, insert_variant, check_listing_exists


def main():
    listings_raw = api_scraper.get_listings()
    brands_dict = generate_brands_dict(listings_raw)

    #TODO: see if processing can be asyncronized

    # for brand in brands_dict:
    #     brand_cars = get_brand_cars(brand, brands_dict)

    brand_cars = get_brand_cars("bmw",brands_dict)

    try:
        load.initialize_tables()
    except ValueError:
        print("table initialization failed")

    for car in brand_cars:
        listing_id = car['id']
        if not check_listing_exists(listing_id):
            load.insert_listing(list(car.values()))
        variant_id = car['variant_id']
        if not check_variant_exists(variant_id):
            variant_info = api_scraper.get_variant_info(variant_id)
            insert_variant(variant_id,variant_info)




if __name__ == "__main__":
    main()



