from pyspark.sql import SparkSession
import os
import time

password = os.environ.get("clickhousepassword")
username = os.getenv("clickhouseusername")

if not password:
        raise ValueError("ClickHouse password not found in environment variables.")
elif not username:
        raise ValueError("ClickHouse username not found in environment variables.")


spark = (
    SparkSession.builder
        .appName("DWH")
        .config("spark.driver.memorty", "1g")
        .config("spark.executor.memory", "1g")
        .config("spark.jars.packages",
                "com.clickhouse.spark:clickhouse-spark-runtime-3.4_2.12:0.8.0,"
                "com.clickhouse:clickhouse-jdbc:0.8.5,"
                "com.clickhouse:clickhouse-http-client:0.8.5")
        .config("spark.sql.catalog.clickhouse", "com.clickhouse.spark.ClickHouseCatalog")
        .config("spark.sql.catalog.clickhouse.host", "xqd059ic56.germanywestcentral.azure.clickhouse.cloud")
        .config("spark.sql.catalog.clickhouse.protocol", "https")
        .config("spark.sql.catalog.clickhouse.http_port", "8443")
        .config("spark.sql.catalog.clickhouse.user", username)
        .config("spark.sql.catalog.clickhouse.password", password)
        .config("spark.sql.catalog.clickhouse.database", "ai_dwh")
        .config("spark.sql.catalog.clickhouse.option.ssl", "true")
        .getOrCreate()
)

df = spark.table("clickhouse.ai_dwh_dwh.gold_sales")

print("\n" + "="*50)
print("now the causeses of the bottelneck...")
print("="*50)
print("\n⏳ Collecting data from ClickHouse...")
start_time = time.time()
result=df.collect()
end_time = time.time()
print(f"✅ finished!")
print(f"⏱️ time: {end_time - start_time:.2f} seconds")

print(f"Number of rows: {len(result)}")


time.sleep(1000)




