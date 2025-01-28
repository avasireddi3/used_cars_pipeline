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

#creating a mapping for how many cars there are in each brand from raw listings response
def generate_brands_dict(listings:dict)->dict:
    brands_dict = {}
    types = ["popular", "luxury", "others"]
    for type in types:
        for brand in listings["data"]["filters"]["brand"]["data"][type]:
            brands_dict[brand["v"]] = brand["c"]
    return brands_dict

#getting a list of all the listed cars by brand
def get_brand_cars(brand:str,brands_dict:dict)->list:
    brand_name = brand
    cnt = brands_dict[brand]
    cars=[]
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
        for car in response['data']['cars']:
            used_car = {
                'id':car['usedCarId'],
                'variant_id':car['centralVariantId'],
                'bodytype':car['bt'],
                'city':car['city'],
                'price':car['msp'],
                'fueltype':car['ft'],
                'mileage':car['km'],
                'make':car['oem'],
                'model':car['model'],
                'gear':car['tt'],
                'owner':car['ownerSlug']
            }
            cars.append(used_car)
    return cars

#get variant info for a given variant id
def get_variant_info(variant_id:int)->list:
    payload = ""
    url = "https://www.cardekho.com/api/v1/usedcar/specs"
    headers = {
        "cookie": "cd_session_id=b4d275df-1a63-4456-8fd4-88da87f0795d; firstUTMParamter=direct%23none%23null",
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36"
    }
    querystring_variant = {f"cityId": "105", "connectoid": "a223ce8e-09eb-2670-52c8-170d94d8ddad",
                           "sessionid": "c99f39fe3c0b18e3a027c0d3791ac0ed", "lang_code": "en", "regionId": "0",
                           "otherinfo": "all", "variantId": {variant_id}}
    response_variant = json.loads(requests.request("GET", url, data=payload, headers=headers, params=querystring_variant).text)
    specs={}
    for item in response_variant['data']['carSpecification']['top']:
        specs[item['key']] = item['value']
    for heading in response_variant['data']['carSpecification']['data']:
        for item in heading['list']:
            specs[item['key']] = item['value']
    variant_spec_names = ('engine_cc','ground_clearance',
                          'mileage_kmpl','drive_type','seating',
                          'power','cylinders','gearbox','top_speed_kmph',
                          'enc','length_mm','width_mm','height_mm')

    spec_names = ('Engine','Ground Clearance Unladen','Mileage',
                    'Drive Type','Seating Capacity','Power','No. of Cylinders',
                    'Gearbox','Top Speed','Emission Norm Compliance','Length',
                    'Width','Height')

    variant_info= {'variant_id': variant_id}

    for i,name in enumerate(variant_spec_names):
        try:
            variant_info[name]=specs[spec_names[i]]
        except KeyError:
            variant_info[name]=0

    return list(variant_info.values())





