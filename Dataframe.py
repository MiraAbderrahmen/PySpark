from pyspark.sql import SparkSession

# Create a SparkSession
spark = SparkSession.builder.appName("DataFrame Example").getOrCreate()

# Create a DataFrame from a list of tuples
data = [(1, "Alice", 30), (2, "Bob", 25), (3, "Charlie", 35)]
columns = ["ID", "Name", "Age"]
df = spark.createDataFrame(data, columns)

df.createOrReplaceTempView("people")


result=spark.sql("SELECT * FROM people WHERE Age > 30")

df_filtered=df.filter(df.Age > 30)
# Show the DataFrame
df.show()
df_filtered.show()
result.show()