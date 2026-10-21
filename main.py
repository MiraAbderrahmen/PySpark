from Spark_jobs.classes.Sparksession import CreateSparkSession
from Spark_jobs.Practice import Practice

if __name__ == "__main__":
    session = CreateSparkSession("Exercise 1", 8, driver_memory="4g", executor_memory="4g")
    spark = session.spark
    try:
        Practice(spark).run()
    finally:
        spark.stop()