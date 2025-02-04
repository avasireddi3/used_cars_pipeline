import requests
import json
from .extract_constants import variants_url,user_headers
from airflow.decorators import task


@task
def variants_data(variant_ids:list):
    """get variants info for a given list of variant ids"""
    payload = ""
    url = variants_url
    headers = user_headers
    variants_info = []
    for variant_id in variant_ids:

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

    return variants_info