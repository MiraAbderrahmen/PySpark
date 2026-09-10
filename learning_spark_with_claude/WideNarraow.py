from classes.Sparksession import CreateSparkSession
import time
SparkSession = CreateSparkSession("WideNarraow",8)
print("spark session created successfully")




#Code without Cashing:
df=SparkSession.spark.read.csv("data/sales_en.csv",header=True)


df_grouped=df.groupBy("category").count().count()

print(df_grouped)
