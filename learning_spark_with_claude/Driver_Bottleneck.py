from time import time
import pickle

from classes.Sparksession import CreateSparkSession, CreateSparkSessionWithConfig
# spark=SparkSession.builder.appName("Slowjob").master("local[*]").getOrCreate()



createsession=CreateSparkSession(app_name="Slowjob",numberof_cores=4)


    


df=createsession.spark.read.csv("data/products_en.csv",header=True)



print(
    "maxPartitionBytes:",
    createsession.spark.conf.get("spark.sql.files.maxPartitionBytes")
)

print("current number of partitions are :",df.rdd.getNumPartitions())




# print(
#     "Rows per partition:",
#     df.rdd.glom().map(len).collect()
# )