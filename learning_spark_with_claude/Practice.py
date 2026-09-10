from classes.Sparksession import CreateSparkSession
import time
from pyspark.sql import functions as F
create_spark_session = CreateSparkSession("Exercise 1", 8,driver_memory="4g",executor_memory="4g")

df = create_spark_session.spark.read.csv("data/sales_en.csv", header=True)

start = time.time()
result1 = df.collect()
time1 = time.time() - start
print(f"collect() time: {time1:.2f}s")


# Code 2:
start = time.time()
result2 = df.groupBy("product_name").agg(F.sum("price")).collect()
time2 = time.time() - start
print(f"groupBy().collect() time: {time2:.2f}s")

# Code 3:
start = time.time()
result3 = df.filter(df.price > 1000).collect()
time3 = time.time() - start
print(f"filter().collect() time: {time3:.2f}s")


time.sleep(1000)