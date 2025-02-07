import requests
import json
import polars as pl
from .extract_constants import listings_url,user_headers
from airflow.decorators import task
from airflow.operators.python import get_current_context


def stage_listings(brand:str,data:list[tuple]):
    df = pl.DataFrame(
        data,
        schema={
            "id": pl.Int32,
            "variant_id": pl.Int32,
            "body_type": pl.String,
            "city": pl.String,
            "price": pl.String,
            "fuel_type": pl.String,
            "mileage": pl.String,
            "make": pl.String,
            "model": pl.String,
            "gear": pl.String,
            "owner": pl.String,
        },
        orient="row",
    )
    df.write_csv(f"/sources/tmp/listings/{brand[0]}_stage_1.csv")



@task(map_index_template="{{brand_name}}")
def listings_data(brand_mapping:tuple)->tuple[str,int]:
    """get listings info for all the cars of a brand"""
    brand_name = brand_mapping[0]
    context = get_current_context()
    context["brand_name"] = brand_name
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
            cars.append(used_car)

    stage_listings(brand_name,cars)

    return brand_name[0],len(cars)
