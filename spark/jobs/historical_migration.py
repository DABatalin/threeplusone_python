from pyspark.sql import SparkSession
from pyspark.sql.functions import current_timestamp

def create_spark_session():
    return (SparkSession.builder
            .appName("Historical Data Migration")
            .config("spark.jars", "/opt/spark/jars/postgresql-42.7.1.jar,/opt/spark/jars/clickhouse-jdbc-0.5.0.jar")
            .config("spark.sql.execution.arrow.pyspark.enabled", "true")
            .getOrCreate())

def migrate_table(spark, table_name, postgres_props, clickhouse_props):
    df = (spark.read
          .format("jdbc")
          .option("driver", "org.postgresql.Driver")
          .option("url", postgres_props["url"])
          .option("dbtable", table_name)
          .option("user", postgres_props["user"])
          .option("password", postgres_props["password"])
          .load())
    
    if "created_at" not in df.columns:
        df = df.withColumn("created_at", current_timestamp())
    
    (df.write
     .format("jdbc")
     .option("driver", "com.clickhouse.jdbc.ClickHouseDriver")
     .option("url", clickhouse_props["url"])
     .option("dbtable", f"ecommerce.{table_name}")
     .option("user", clickhouse_props.get("user", "default"))
     .option("password", clickhouse_props.get("password", ""))
     .mode("append")
     .save())

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
    
    spark = create_spark_session()
    
    try:
        for table in tables:
            print(f"Migrating table: {table}")
            migrate_table(spark, table, postgres_props, clickhouse_props)
            print(f"Successfully migrated table: {table}")
    except Exception as e:
        print(f"Error during migration: {e}")
    finally:
        spark.stop()

if __name__ == "__main__":
    main() 