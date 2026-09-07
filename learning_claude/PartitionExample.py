from pyspark.sql import SparkSession
import time
import os

print(os.cpu_count())

spark=SparkSession.builder.appName("PartitionExample").master("local[4]").getOrCreate()