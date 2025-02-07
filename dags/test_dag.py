from airflow.decorators import dag
from airflow.providers.common.sql.operators.sql import SQLExecuteQueryOperator
from pendulum import datetime
from lib.extract.extract_brand_mapping import extract_brand_mapping
from lib.extract.extract_listings import extract_stage_listings
from lib.extract.extract_variants import extract_variants
from lib.transform.transform_stage_listings import transform_stage_listings
from lib.transform.transform_load_variants import transform_load_variants
from lib.load.load_listings import load_listings

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
        sql = "sql/find_new_listings.sql"
    )

    find_new_variants = SQLExecuteQueryOperator(
        task_id = "find_new_variants",
        conn_id = "postgres_default",
        sql = "sql/find_new_variants.sql"
    )

    insert_new_listings = SQLExecuteQueryOperator(
        task_id = "insert_new_listings",
        conn_id = "postgres_default",
        sql = "sql/update_new_listings.sql"
    )

    update_sold_listings = SQLExecuteQueryOperator(
        task_id = "update_sold_listings",
        conn_id = "postgres_default",
        sql = "sql/update_sold_listings.sql"
    )

    update_unsold_listings = SQLExecuteQueryOperator(
        task_id = "update_unsold_listings",
        conn_id = "postgres_default",
        sql = "sql/update_unsold_listings.sql"
    )

    brands = extract_brand_mapping()
    data = extract_stage_listings.expand(brand_mapping=brands)
    transformed_data = transform_stage_listings.expand(passed=data)
    variants = extract_variants()

    transformed_data >> load_listings() >> init_tables >> [find_new_listings, find_new_variants]
    find_new_listings>>[update_sold_listings,update_unsold_listings,insert_new_listings]
    find_new_variants>>variants
    transform_load_variants(variants)


test_workflow()