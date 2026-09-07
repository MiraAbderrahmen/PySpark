from pyspark.sql import SparkSession


spark=(
    SparkSession.builder
    .master("local[4]") # Use 4 cores for local testing
    .appName("SparkPartitioningExample")
    .getOrCreate()
)


# df=spark.range(1,20)
# print(df.rdd.getNumPartitions())

# print(df.rdd.glom().collect())

# filterd_df=df.filter(df.id>10)
# print(filterd_df.rdd.glom().collect())



df1 = spark.createDataFrame(
    [
        (1, "A"),
        (2, "B"),
        (3, "A"),
        (4, "B"),
        (5, "A"),
        (6, "C"),
        (7, "C"),
        (8, "B"),
    ],
    ["id", "category"]
)


# print(df1.rdd.glom().collect())  # Show the data in each partition

result = df1.groupBy("category").count()

print(result.rdd.glom().collect())  # Show the data in each partition after groupBy