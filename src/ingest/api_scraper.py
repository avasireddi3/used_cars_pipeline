import requests
import json
import type_classes

def get_listings()->dict:
    #url to get listings info
    url = "https://listing.cardekho.com/api/v1/srp-listings"
    payload=""
    #headers for the request
    headers = {
            "cookie": "cd_session_id=b4d275df-1a63-4456-8fd4-88da87f0795d; firstUTMParamter=direct%23none%23null",
            "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36"
        }
    #query details specifying that we want all the cars in bengaluru
    querystring = {"cityId":"105",
                   "connectoid":"a223ce8e-09eb-2670-52c8-170d94d8ddad",
                   "sessionid":"c99f39fe3c0b18e3a027c0d3791ac0ed",
                   "lang_code":"en",
                   "regionId":"0",
                   "searchstring":"used-cars+in+bangalore",
                   "pagefrom":"0",
                   "sortby":"created_date",
                   "sortorder":"desc",
                   "mink":"",
                   "maxk":"",
                   "dealer_id":"null",
                   "regCityNames":"",
                   "regStateNames":"",
                   "cellValue":"",
                   "pagination":"{}",
                   "carsAd":"[]",
                   "device":"web",
                   "userLat":"",
                   "userLng":""}
    #getting response in the form of a dictionary from a json using the parameters specified above
    response = json.loads(requests.request("GET", url, data=payload, headers=headers, params=querystring).text)
    return response

#creating a mapping for how many cars there are in each brand from listings info
def generate_brands_dict(listing_info:dict)->dict:
    brands_dict = {}
    types = ["popular", "luxury", "others"]
    for type in types:
        for brand in listing_info["data"]["filters"]["brand"]["data"][type]:
            brands_dict[brand["v"]] = brand["c"]
    return brands_dict

#getting a list of all the listed cars by brand
def get_brand_cars(brand:str,brands_dict:dict)->dict:
    brand_name = brand
    cnt = brands_dict[brand]
    url = "https://listing.cardekho.com/api/v1/srp-listings"
    payload=""
    headers = {
        "cookie": "cd_session_id=b4d275df-1a63-4456-8fd4-88da87f0795d; firstUTMParamter=direct%23none%23null",
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36"
    }
    for i in range(0, cnt, 20):
        frompage = i
        querystring = {f"cityId": "105",
                       "connectoid": "a223ce8e-09eb-2670-52c8-170d94d8ddad",
                       "sessionid": "c99f39fe3c0b18e3a027c0d3791ac0ed",
                       "lang_code": "en",
                       "regionId": "0",
                       "searchstring": {brand_name},
                       "pagefrom": {frompage},
                       "sortby": "created_date",
                       "sortorder": "desc",
                       "mink": "",
                       "maxk": "",
                       "dealer_id": "null",
                       "regCityNames": "",
                       "regStateNames": "",
                       "cellValue": "",
                       "pagination": "{\"common\":0,\"commonFeature\":0,\"carAd\":0}",
                       "carsAd": "[]", "device": "web",
                       "userLat": "", "userLng": ""}
        response = json.loads(requests.request("GET", url, data=payload, headers=headers, params=querystring).text)
        return response

#get variant info for a given variant id
def get_variant_info(variantid:int)->dict:
    payload = ""
    headers = {
        "cookie": "cd_session_id=b4d275df-1a63-4456-8fd4-88da87f0795d; firstUTMParamter=direct%23none%23null",
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36"
    }
    querystring_variant = {f"cityId": "105", "connectoid": "a223ce8e-09eb-2670-52c8-170d94d8ddad",
                           "sessionid": "c99f39fe3c0b18e3a027c0d3791ac0ed", "lang_code": "en", "regionId": "0",
                           "otherinfo": "all", "variantId": {variantid}}
    response_variant = json.loads(requests.request("GET", url, data=payload, headers=headers, params=querystring_variant).text)
    return response_variant





