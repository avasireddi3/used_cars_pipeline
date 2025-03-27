import json
import logging
import requests
import urllib
import cloudscraper
from data_models import Listing
from rich import print

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

headers = {
    "accept": "*/*",
    "accept-language": "en-US,en;q=0.9",
    "content-type": "application/json",
    "origin": "https://www.spinny.com",
    "platform": "web",
    "priority": "u=1, i",
    "procurement-category": "assured,luxury",
    "referer": "https://www.spinny.com/",
    "sec-ch-ua": """Not:A-Brand";v="24", "Chromium";v="134""",
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": "Linux",
    "sec-fetch-dest": "empty",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "same-site",
    "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36"
}

def get_response(auth:dict)->requests.models.Response:
    """"getting response from backend api for a given query and response"""
    logger.debug("Getting response")
    scraper = cloudscraper.create_scraper()
    params = {"city":"bangalore",
               "product_type":"cars",
               "category":"used",
               "page":"1",
               "show_max_on_assured":"true",
               "custom_budget_sort":"true",
               "ratio_status":"available",
               "size":"500",
               "total_count":"1294",
               "exclude_ids_v2":"19177757,19122530",
               "prioritize_filter_listing":"true",
               "high_intent_required":"true",
               "active_banner":"true",
               "is_max_certified":"0"}
    base_url = "https://api.spinny.com/v3/api/listing/v3/"
    encoded_params = urllib.parse.urlencode(params)
    complete_url = f"{base_url}?{encoded_params}"
    resp = scraper.get(url=complete_url,
                       headers=auth,allow_redirects=True)
    return resp


def extract(data:dict)->list[Listing]:
    listings = []
    for i,item in enumerate(data["results"]):
        listing_id = str(item["id"])
        listing_name = item["make"] + item["model"] + item["variant"]
        model_name = item["model"] + item["variant"]
        model_id = str(i)
        make_name = item["make"]
        price = item["price"]
        mileage = item["mileage"]
        transmission = item["transmission"]
        fuel = item["fuel_type"]
        listings.append(Listing(
            listing_id=listing_id,
            listing_name=listing_name,
            model_name=model_name,
            model_id=model_id,
            make_name=make_name,
            price=price,
            mileage=mileage,
            transmission=transmission,
            fuel=fuel
        ))
    return listings
def main():
    resp = get_response(headers)
    data = json.loads(resp.text)
    # with open("spinny_sample.json","w") as f:
    #     f.write(json.dumps(data,indent=2))
    listings = extract(data)
    for listing in listings:
        print(listing)

if __name__=="__main__":
    main()