import json
from src.ingest import api_scraper
from src.ingest.api_scraper import generate_brands_dict, get_brand_cars


def main():
    listings_raw = api_scraper.get_listings()
    brands_dict = generate_brands_dict(listings_raw)

    #TODO: see if processing can be asyncronized
    for brand in brands_dict:
        brand_cars = get_brand_cars(brand, brands_dict)
        for car in brand_cars[:1]:
            print(json.dumps(car, indent=4))



if __name__ == "__main__":
    main()



