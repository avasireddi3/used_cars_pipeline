import requests
import json
from .extract_constants import listings_url,user_headers
from airflow.decorators import task


def extract_brands_mapping(listings: dict) -> list[tuple]:
    """generate a mapping of brand to number of listings"""
    brands_mapping = []
    brand_types = ["popular", "luxury", "others"]
    for brand_type in brand_types:
        for brand in listings["data"]["filters"]["brand"]["data"][brand_type]:
            brands_mapping.append(([brand["v"]], brand["c"]))
    return brands_mapping

@task
def brand_mapping() -> list[tuple]:
    """extract mapping of brands to number of listings from api"""
    # url to get listings info
    url = listings_url
    payload = ""
    # headers for the request
    headers = user_headers
    # query details specifying that we want all the cars in bengaluru
    querystring = {
        "cityId": "105",
        "connectoid": "a223ce8e-09eb-2670-52c8-170d94d8ddad",
        "sessionid": "c99f39fe3c0b18e3a027c0d3791ac0ed",
        "lang_code": "en",
        "regionId": "0",
        "searchstring": "used-cars+in+bangalore",
        "pagefrom": "0",
        "sortby": "created_date",
        "sortorder": "desc",
        "mink": "",
        "maxk": "",
        "dealer_id": "null",
        "regCityNames": "",
        "regStateNames": "",
        "cellValue": "",
        "pagination": "{}",
        "carsAd": "[]",
        "device": "web",
        "userLat": "",
        "userLng": "",
    }
    # getting response in the form of a dictionary
    # from a json using the parameters specified above
    response = json.loads(
        requests.request(
            "GET", url, data=payload, headers=headers, params=querystring
        ).text
    )

    brands_mapping = extract_brands_mapping(response)

    return brands_mapping[15:16]




