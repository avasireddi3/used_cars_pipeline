import requests
import json
from .extract_constants import variants_url,user_headers
from airflow.decorators import task
import polars as pl
from sqlalchemy import create_engine

@task
def variants_data(**context):
    """get variants info for a given list of variant ids"""
    payload = ""
    url = variants_url
    headers = user_headers
    variants_info = []
    variant_ids = context['ti'].xcom_pull(task_ids='find_new_variants',key='return_value')
    for variant_id in variant_ids:
        variant_id = variant_id[0]
        querystring_variant = {
            "cityId": "105",
            "connectoid": "a223ce8e-09eb-2670-52c8-170d94d8ddad",
            "sessionid": "c99f39fe3c0b18e3a027c0d3791ac0ed",
            "lang_code": "en",
            "regionId": "0",
            "otherinfo": "all",
            "variantId": variant_id,
        }

        response_variant = json.loads(
            requests.request(
                "GET", url, data=payload, headers=headers, params=querystring_variant
            ).text
        )
        specs = {}
        for item in response_variant["data"]["carSpecification"]["top"]:
            specs[item["key"]] = item["value"]
        for heading in response_variant["data"]["carSpecification"]["data"]:
            for item in heading["list"]:
                specs[item["key"]] = item["value"]
        variant_spec_names = (
            "engine_cc",
            "ground_clearance",
            "mileage_kmpl",
            "drive_type",
            "seating",
            "power",
            "cylinders",
            "gearbox",
            "top_speed_kmph",
            "enc",
            "length_mm",
            "width_mm",
            "height_mm",
        )

        spec_names = (
            "Engine",
            "Ground Clearance Unladen",
            "Mileage",
            "Drive Type",
            "Seating Capacity",
            "Power",
            "No. of Cylinders",
            "Gearbox",
            "Top Speed",
            "Emission Norm Compliance",
            "Length",
            "Width",
            "Height",
        )

        variant_info = {"variant_id": variant_id}

        for i, name in enumerate(variant_spec_names):
            try:
                variant_info[name] = specs[spec_names[i]]
            except KeyError:
                variant_info[name] = 0

        variants_info.append(list(variant_info.values()))
    variants_df = pl.DataFrame(data=variants_info,
                               schema={
                                   "variant_id": pl.Int32,
                                   "engine_cc": pl.String,
                                   "ground_clearance_mm": pl.String,
                                   "mileage_kmpl": pl.String,
                                   "drive_type": pl.String,
                                   "seating_capacity": pl.String,
                                   "power": pl.String,
                                   "cylinders": pl.String,
                                   "gearbox": pl.String,
                                   "top_speed_kmph": pl.String,
                                   "enc": pl.String,
                                   "length_mm": pl.String,
                                   "width_mm": pl.String,
                                   "height_mm": pl.String,
                               },
                                orient='row',)
    variants_df.write_csv("/sources/tmp/variants/new_variants.csv")

    return f"loaded {len(variants_info)} new variants"