from pyspark.sql import SparkSession
from pyspark.sql.functions import col, current_timestamp
from datetime import datetime, timedelta

def create_spark_session():
    return (SparkSession.builder
            .appName("Incremental Data Sync")
            .config("spark.jars", "/opt/spark/jars/postgresql-42.7.1.jar,/opt/spark/jars/clickhouse-jdbc-0.5.0.jar")
            .config("spark.sql.execution.arrow.pyspark.enabled", "true")
            .getOrCreate())

def sync_table(spark, table_name, postgres_props, clickhouse_props, last_sync_time):
    query = f"""
    SELECT * FROM {table_name} 
    WHERE created_at >= '{last_sync_time}'
    OR updated_at >= '{last_sync_time}'
    """
    
    df = (spark.read
          .format("jdbc")
          .option("driver", "org.postgresql.Driver")
          .option("url", postgres_props["url"])
          .option("query", query)
          .option("user", postgres_props["user"])
          .option("password", postgres_props["password"])
          .load())
    
    if df.count() > 0:
        (df.write
         .format("jdbc")
         .option("driver", "com.clickhouse.jdbc.ClickHouseDriver")
         .option("url", clickhouse_props["url"])
         .option("dbtable", f"ecommerce.{table_name}")
         .option("user", clickhouse_props.get("user", "default"))
         .option("password", clickhouse_props.get("password", ""))
         .mode("append")
         .save())
        
        print(f"Synced {df.count()} records for table {table_name}")
    else:
        print(f"No new records to sync for table {table_name}")

def main():
    postgres_props = {
        "url": "jdbc:postgresql://db:5432/ecommerce",
        "user": "postgres",
        "password": "postgres"
    }
    
    clickhouse_props = {
        "url": "jdbc:clickhouse://clickhouse:8123/ecommerce"
    }
    
    tables = [
        "users",
        "products",
        "categories",
        "sellers",
        "sales",
        "product_ratings",
        "seller_ratings",
        "cart_items"
    ]
    
    last_sync_time = (datetime.now() - timedelta(hours=1)).strftime('%Y-%m-%d %H:%M:%S')
    
    spark = create_spark_session()
    
    try:
        for table in tables:
            print(f"Syncing table: {table}")
            sync_table(spark, table, postgres_props, clickhouse_props, last_sync_time)
    except Exception as e:
        print(f"Error during sync: {e}")
    finally:
        spark.stop()

if __name__ == "__main__":
    main() 