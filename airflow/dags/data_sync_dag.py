from airflow import DAG
from airflow.providers.apache.spark.operators.spark_submit import SparkSubmitOperator
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
import requests

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2024, 1, 1),
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5)
}

def check_data_quality():
    """
    Simple data quality check function
    """
    clickhouse_url = "http://clickhouse:8123"
    
    queries = [
        "SELECT count(*) FROM ecommerce.sales",
        "SELECT count(*) FROM ecommerce.user_sessions",
        "SELECT count(*) FROM ecommerce.daily_sales_aggregation"
    ]
    
    for query in queries:
        try:
            response = requests.post(
                clickhouse_url,
                params={'query': query},
                timeout=10
            )
            if response.status_code != 200:
                raise Exception(f"Query failed: {query}")
            count = int(response.text.strip())
            if count == 0:
                raise Exception(f"No data found for query: {query}")
        except Exception as e:
            raise Exception(f"Data quality check failed: {str(e)}")

with DAG(
    'data_sync_and_aggregation',
    default_args=default_args,
    description='Sync data from PostgreSQL to ClickHouse and run aggregations',
    schedule_interval=timedelta(hours=1),
    catchup=False
) as dag:

    sync_task = SparkSubmitOperator(
        task_id='incremental_sync',
        application='/opt/spark/jobs/incremental_sync.py',
        conn_id='spark_default',
        conf={
            'spark.driver.memory': '1g',
            'spark.executor.memory': '1g'
        }
    )

    aggregation_task = SparkSubmitOperator(
        task_id='data_aggregation',
        application='/opt/spark/jobs/data_aggregation.py',
        conn_id='spark_default',
        conf={
            'spark.driver.memory': '1g',
            'spark.executor.memory': '1g'
        }
    )

    quality_check = PythonOperator(
        task_id='data_quality_check',
        python_callable=check_data_quality
    )

    sync_task >> aggregation_task >> quality_check

with DAG(
    'historical_data_migration',
    default_args=default_args,
    description='One-time historical data migration from PostgreSQL to ClickHouse',
    schedule_interval=None,
    catchup=False
) as historical_dag:

    migration_task = SparkSubmitOperator(
        task_id='historical_migration',
        application='/opt/spark/jobs/historical_migration.py',
        conn_id='spark_default',
        conf={
            'spark.driver.memory': '2g',
            'spark.executor.memory': '2g'
        }
    )

    migration_quality_check = PythonOperator(
        task_id='migration_quality_check',
        python_callable=check_data_quality
    )

    migration_task >> migration_quality_check 