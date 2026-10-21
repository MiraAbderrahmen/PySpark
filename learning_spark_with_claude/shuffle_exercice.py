from classes.Sparksession import CreateSparkSession

import pyspark.sql.functions as F
import time


spark_session = CreateSparkSession("ShuffleExample", 4)
spark = spark_session.spark
df=spark.read.csv("data/sales_en.csv", header=True, inferSchema=True)
 
start = time.time()
df.filter(F.col("price") > 100)\
     .groupBy("city")\
     .agg(F.sum("quantity_sold"))\
     .explain()
time2 = time.time() - start
time.sleep(1000)
