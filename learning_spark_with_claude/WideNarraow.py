from classes.Sparksession import CreateSparkSession
import time
SparkSession = CreateSparkSession("WideNarraow",4)
print("spark session created successfully")




#Code without Cashing:
df=SparkSession.spark.read.csv("data/sales_en.csv",header=True).count()

print("Total number of records in the dataset: ",df)