from unittest import result

from pyspark.sql import SparkSession
import inspect
import time

spark = SparkSession.builder \
    .appName("BasicPySparkApp") \
    .master("local[*]") \
    .getOrCreate()

data = [
    ("Alice", 34),
    ("Bob", 45),
    ("Charlie", 29),
    ("Diana", 40)
]

columns = ["name", "age"]


#print(inspect.getsource(spark.createDataFrame))

df = spark.createDataFrame(data, columns)
df.filter(df.age > 30).show()  # 🔥 ACTION → triggers Spark job

print("Initial DataFrame:")
df.show()
df.collect()  # 🔥 ACTION → creates Spark job
print("DataFrame schema:")
# Filter
df_filtered = df.filter(df.age > 30)
df_filtered.show()  # 🔥 ACTION → another job

# GroupBy aggregation (shuffle happens here)
avg_age = df.groupBy().avg("age")
avg_age.show()  # 🔥 ACTION → triggers shuffle stage

result = df.groupBy().avg("age")
result.explain("formatted")

print("Sleeping so you can open Spark UI...")
time.sleep(1000)

spark.stop()
