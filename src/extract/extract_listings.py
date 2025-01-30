import requests
import json


def extract_brands_mapping(listings: dict) -> dict:
    """generate a mapping of brand to number of listings"""
    brands_mapping = {}
    brand_types = ["popular", "luxury", "others"]
    for brand_type in brand_types:
        for brand in listings["data"]["filters"]["brand"]["data"][brand_type]:
            brands_mapping[brand["v"]] = brand["c"]
    return brands_mapping

def extract_listings_info() -> dict:
    """extract mapping of brands to number of listings from api"""
    # url to get listings info
    url = "https://listing.cardekho.com/api/v1/srp-listings"
    payload = ""
    # headers for the request
    headers = {
        "cookie": """cd_session_id=b4d275df-1a63-4456-8fd4-88da87f0795d;
        firstUTMParamter=direct%23none%23null""",
        "User-Agent": """Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36
        (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36""",
    }
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

    return brands_mapping

def extract_listings_data(brand: str, brands_mapping:dict)->list:
    """get listings info for all the cars of a brand"""
    brand_name = brand
    cnt = brands_mapping[brand]
    cars = []
    url = "https://listing.cardekho.com/api/v1/srp-listings"
    payload = ""
    headers = {
        "cookie": """cd_session_id=b4d275df-1a63-4456-8fd4-88da87f0795d;
            firstUTMParamter=direct%23none%23null""",
        "User-Agent": """Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36
            (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36""",
    }
    for i in range(0, cnt, 20):
        from_page = i
        querystring = {
            "cityId": "105",
            "connectoid": "a223ce8e-09eb-2670-52c8-170d94d8ddad",
            "sessionid": "c99f39fe3c0b18e3a027c0d3791ac0ed",
            "lang_code": "en",
            "regionId": "0",
            "searchstring": brand_name,
            "pagefrom": from_page,
            "sortby": "created_date",
            "sortorder": "desc",
            "mink": "",
            "maxk": "",
            "dealer_id": "null",
            "regCityNames": "",
            "regStateNames": "",
            "cellValue": "",
            "pagination": '{"common":0,"commonFeature":0,"carAd":0}',
            "carsAd": "[]",
            "device": "web",
            "userLat": "",
            "userLng": "",
        }
        response = json.loads(
            requests.request(
                "GET", url, data=payload, headers=headers, params=querystring
            ).text
        )
        for car in response["data"]["cars"]:
            used_car = [
                car["usedCarId"],
                car["centralVariantId"],
                car["bt"],
                car["city"],
                car["msp"],
                car["ft"],
                car["km"],
                car["oem"],
                car["model"],
                car["tt"],
                car["ownerSlug"],
            ]
            cars.append(used_car)
    return cars



