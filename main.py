import sys
from pyspark.sql import SparkSession
from Spark_jobs.Practice import Practice
if __name__ == "__main__":
    spark = SparkSession.builder.appName("Practice").getOrCreate()
    practice = Practice(spark)
    practice.run()