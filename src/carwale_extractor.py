import json
import logging
import requests
import cloudscraper
from data_models import Listing
from rich import print

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

headers = {
    "accept": "*/*",
    "accept-language": "en-US,en;q=0.9",
    "content-type": "application/json",
    "origin": "https://www.carwale.com",
    "priority": "u=1, i",
    "referer": "https://www.carwale.com/used/bangalore/",
    "requestverificationtoken": "CfDJ8JUh_GoNOjhBqUJ2d7OuCzRqMrJpn4rkYqcg-S9dEwokjFI9yxnrZmvvyp8gUy9KVzIlWARTMkYFzx5QbOwtRO5ZpfuvnsS8JRrsxCpT09CNLSQrsIEH6EhWLHKvtyP23jbL2DxWbfwzdEXgbx6xccA",
    "sec-ch-ua": """Not:A-Brand";v="24", "Chromium";v="134""",
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": "Linux",
    "sec-fetch-dest": "empty",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "same-origin",
    "serverdomain": "CarWale",
    "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36",
}

def get_response(auth:dict)->requests.models.Response:
    """"getting response from backend api for a given query and response"""
    logger.debug("Getting response")
    scraper = cloudscraper.create_scraper()
    body = {
    "pn": "1",
    "city": "2",
    "ps": "60",
    "sc": "-1",
    "so": "-1",
    "lcr": 24,
    "shouldfetchnearbycars": "False",
    "stockfetched": "32",
    }
    base_url = "https://www.carwale.com/api/stocks/filters/"
    # encoded_params = urllib.parse.urlencode(params)
    # complete_url = f"{base_url}?{encoded_params}"
    resp = scraper.post(url=base_url,
                       headers=auth,json=body)
    return resp

def extract(data:dict)->list[Listing]:
    listings = []
    for item in data["stocks"]:
        listing_id = item["profileId"]
        listing_name = item["carName"]
        model_name = item["modelName"]
        model_id =  item["modelId"]
        make_name = item["makeName"]
        price = item["priceNumeric"]
        mileage = item["kmNumeric"]
        transmission = item["transmission"]
        fuel = item["fuel"]
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
    # with open("carwale_sample.json","w") as f:
    #     f.write(json.dumps(data,indent=2))
    listings = extract(data)
    for listing in listings:
        print(listing)

if __name__=="__main__":
    main()