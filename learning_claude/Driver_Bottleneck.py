from pyspark.sql import SparkSession
from time import time
import pickle
spark=SparkSession.builder.appName("Slowjob").master("local[*]").getOrCreate()


df=spark.read.csv("data/products_en.csv",header=True)




print("current number of partitions are :",df.rdd.getNumPartitions())
max_bytes = spark.conf.get("spark.sql.files.maxPartitionBytes")

print("Max partition bytes:", max_bytes)
print("Max partition MB:", int(max_bytes) / (1024 * 1024))


# print(
#     "Rows per partition:",
#     df.rdd.glom().map(len).collect()
# )