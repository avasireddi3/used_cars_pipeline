from airflow.decorators import dag
from airflow.providers.common.sql.operators.sql import SQLExecuteQueryOperator
from airflow.models.baseoperator import chain, chain_linear
from pendulum import datetime
from lib.load.load_listings import read_data
from lib.extract.extract_brand_mapping import brand_mapping
from lib.extract.extract_listings_data import listings_data
from lib.extract.extract_variants import variants_data
from lib.transform.transform_listings import full_transform_listings
from lib.transform.transform_variants import full_transform_variants
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
        sql = "sql/insert_new_listings.sql"
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

    brands = brand_mapping()
    data = listings_data.expand(brand_mapping=brands)
    transformed_data = full_transform_listings.expand(passed=data)
    variants = variants_data()
    # chain_linear(transformed_data
    #  ,insert_data()
    #  ,init_tables
    #  ,[find_new_listings,find_new_variants]
    #  ,[update_sold_listings,
    #    update_unsold_listings,
    #    insert_new_listings,
    #    variants_data()]
    #  ,full_transform_variants())
    transformed_data>>insert_data()>>init_tables>>[find_new_listings,find_new_variants]
    find_new_listings>>[update_sold_listings,update_unsold_listings,insert_new_listings]
    find_new_variants>>variants
    full_transform_variants(variants)


test_workflow()