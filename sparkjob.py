from pyspark.sql import SparkSession

# 1️⃣ إنشاء SparkSession
spark = SparkSession.builder \
    .appName("PySpark DAG Example") \
    .master("local[2]") \
    .getOrCreate()

# 2️⃣ إنشاء RDD مقسم على 2 partitions
rdd = spark.sparkContext.parallelize([1,2,3,4,5,6], 2)  # 2 partitions

# 3️⃣ Transformation 1: multiply by 2
rdd2 = rdd.map(lambda x: x*2)

# 4️⃣ Transformation 2: keep only values > 5
rdd3 = rdd2.filter(lambda x: x>5)

# 5️⃣ شوف DAG / execution plan (logical + physical plan)
print("=== DAG / Execution Plan ===")
print(rdd3.toDebugString().decode('utf-8'))  # هنا بنشوف ال DAG بتاعنا
# 6️⃣ Action: collect results
print("=== Result ===")
print(rdd3.collect())  # هنا Driver يجمع النتائج من executors

# 7️⃣ إغلاق SparkSession
spark.stop()