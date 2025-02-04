from airflow.decorators import dag
from pendulum import datetime
from lib.extract.extract_brand_mapping import brand_mapping
from lib.extract.extract_listings_data import listings_data
from lib.transform.transform_listings import full_transform

@dag(
    start_date=datetime(2024,2,1),
    max_active_runs=2,
    schedule="@daily",
    catchup=False
)
def test_workflow():

    print(brand_mapping())
    full_transform.expand(
        data=listings_data.expand(
            brand_mapping=brand_mapping()))




test_workflow()