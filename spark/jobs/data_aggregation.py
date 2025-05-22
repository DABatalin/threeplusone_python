from pyspark.sql import SparkSession
from pyspark.sql.functions import col, count, sum, avg, window, current_timestamp

def create_spark_session():
    return (SparkSession.builder
            .appName("Data Aggregation")
            .config("spark.jars", "/opt/spark/jars/clickhouse-jdbc-0.5.0.jar")
            .config("spark.sql.execution.arrow.pyspark.enabled", "true")
            .getOrCreate())

def aggregate_sales_data(spark, clickhouse_props):
    # Read from ClickHouse
    sales_df = (spark.read
                .format("jdbc")
                .option("driver", "com.clickhouse.jdbc.ClickHouseDriver")
                .option("url", clickhouse_props["url"])
                .option("dbtable", "ecommerce.sales")
                .option("user", clickhouse_props.get("user", "default"))
                .option("password", clickhouse_props.get("password", ""))
                .load())
    
    # Daily sales aggregation
    daily_sales = (sales_df
                  .groupBy(window(col("sale_date"), "1 day"))
                  .agg(
                      count("sale_id").alias("total_sales"),
                      sum("quantity").alias("total_quantity"),
                      sum(col("price_at_sale") * col("quantity")).alias("total_revenue")
                  ))
    
    # Write daily aggregations to ClickHouse
    (daily_sales.write
     .format("jdbc")
     .option("driver", "com.clickhouse.jdbc.ClickHouseDriver")
     .option("url", clickhouse_props["url"])
     .option("dbtable", "ecommerce.daily_sales_aggregation")
     .option("user", clickhouse_props.get("user", "default"))
     .option("password", clickhouse_props.get("password", ""))
     .mode("append")
     .save())

def aggregate_user_activity(spark, clickhouse_props):
    # Read from ClickHouse
    sessions_df = (spark.read
                  .format("jdbc")
                  .option("driver", "com.clickhouse.jdbc.ClickHouseDriver")
                  .option("url", clickhouse_props["url"])
                  .option("dbtable", "ecommerce.user_sessions")
                  .option("user", clickhouse_props.get("user", "default"))
                  .option("password", clickhouse_props.get("password", ""))
                  .load())
    
    # User activity aggregation
    user_activity = (sessions_df
                    .groupBy("user_id")
                    .agg(
                        count("session_id").alias("total_sessions"),
                        sum("click_count").alias("total_clicks"),
                        avg("click_count").alias("avg_clicks_per_session")
                    ))
    
    # Write user activity aggregations to ClickHouse
    (user_activity.write
     .format("jdbc")
     .option("driver", "com.clickhouse.jdbc.ClickHouseDriver")
     .option("url", clickhouse_props["url"])
     .option("dbtable", "ecommerce.user_activity_aggregation")
     .option("user", clickhouse_props.get("user", "default"))
     .option("password", clickhouse_props.get("password", ""))
     .mode("append")
     .save())

def main():
    clickhouse_props = {
        "url": "jdbc:clickhouse://clickhouse:8123/ecommerce"
    }
    
    spark = create_spark_session()
    
    try:
        print("Starting sales data aggregation...")
        aggregate_sales_data(spark, clickhouse_props)
        print("Sales data aggregation completed")
        
        print("Starting user activity aggregation...")
        aggregate_user_activity(spark, clickhouse_props)
        print("User activity aggregation completed")
    except Exception as e:
        print(f"Error during aggregation: {e}")
    finally:
        spark.stop()

if __name__ == "__main__":
    main() 