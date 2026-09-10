from classes.Sparksession import CreateSparkSession
import time
SparkSession = CreateSparkSession("ActionTrans",8)
print("spark session created successfully")

# an Action is an operation that forces( triggers) the execution of the previous steps 
#df.show(), count(), take(), collect() are all actions that trigger the execution of the previous steps


# Each Action is completely indepenedet

#Code without Cashing:
df=SparkSession.spark.read.csv("data/sales_en.csv",header=True)

df_filtered=df.filter(df["total_amount"] > 1000)
df_filtered.cache() #cashing the filtered data to avoid recomputation of the same data multiple times

start=time.perf_counter()
result1= df_filtered.show()
end=time.perf_counter()
print("Time taken without cashing is : ",end-start)

start=time.perf_counter()
result2= df_filtered.count()
end=time.perf_counter()
print("Time taken without cashing is : ",end-start)

start=time.perf_counter()
result3= df_filtered.count()
end=time.perf_counter()
print("Time taken without cashing is : ",end-start)

# # SE cache() when:
# - Same transformation used multiple times
# - Expensive operation (join, groupBy, etc)
# - Want to reuse results across multiple action



df_expensive=df.filter(df["total_amount"] > 1000).groupBy("category").count().cache()
df_expensive.show()
df_expensive.orderBy("count").show()