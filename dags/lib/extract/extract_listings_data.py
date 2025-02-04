import requests
import json
from .extract_constants import listings_url,user_headers
from airflow.decorators import task


@task
def listings_data(brand_mapping:tuple)->list[tuple]:
    """get listings info for all the cars of a brand"""
    brand_name = brand_mapping[0]
    cnt = brand_mapping[1]
    cars = []
    url = listings_url
    payload = ""
    headers = user_headers
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
            used_car = (
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
            )
            print(used_car)
            cars.append(used_car)

    return cars
