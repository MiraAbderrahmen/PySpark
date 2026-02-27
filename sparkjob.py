from pyspark.sql import SparkSession

# 1️⃣ Create SparkSession
spark = SparkSession.builder \
    .appName("Two Stages Example") \
    .master("local[2]") \
    .getOrCreate()

# 2️⃣ Create RDD with 2 partitions
rdd = spark.sparkContext.parallelize([("a",1),("b",1),("a",1),("b",1),("c",1),("c",1)], 2)

# 3️⃣ Narrow transformation (stage 1)
rdd2 = rdd.map(lambda x: (x[0], x[1]*2))  # multiply values by 2

# 4️⃣ Wide transformation (stage 2, causes shuffle)
counts = rdd2.reduceByKey(lambda a,b: a+b)

# 5️⃣ Action
print(counts.collect())

# 6️⃣ Stop SparkSession
spark.stop()