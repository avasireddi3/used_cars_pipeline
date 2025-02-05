from airflow.decorators import dag
from airflow.providers.common.sql.operators.sql import SQLExecuteQueryOperator
from pendulum import datetime
from lib.load.load_listings import read_data
from lib.extract.extract_brand_mapping import brand_mapping
from lib.extract.extract_listings_data import listings_data
from lib.transform.transform_listings import full_transform
from lib.load.load_listings import insert_data

@dag(
    start_date=datetime(2024,2,1),
    max_active_runs=2,
    schedule="@daily",
    catchup=False
)
def test_workflow():

    init_tables = SQLExecuteQueryOperator(
        task_id="initialize_tables",
        conn_id="postgres_default",
        sql="sql/init_tables.sql"
    )

    find_new_listings = SQLExecuteQueryOperator(
        task_id = "find_new_listings",
        conn_id = "postgres_default",
        sql = "sql/new_listings.sql"
    )
    brands = brand_mapping()
    data = listings_data.expand(brand_mapping=brands)
    (full_transform.expand(passed=data)
        >>insert_data()
        >>read_data()
        >>init_tables
        >>find_new_listings)




test_workflow()