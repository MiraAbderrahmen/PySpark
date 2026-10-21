from classes.Sparksession import CreateSparkSession
import time
from pyspark.sql import functions as F
create_spark_session = CreateSparkSession("Exercise 1", 8,driver_memory="4g",executor_memory="4g")

df = create_spark_session.spark.read.csv("data/sales_en.csv", header=True)

# Code 3:
start = time.time()
result3 = df.filter(df.price > 1000)
time3 = time.time() - start
print(f"filter() time: {time3:.2f}s")


time.sleep(1000)