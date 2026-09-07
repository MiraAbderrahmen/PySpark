"""
COMPREHENSIVE GUIDE TO SPARK SHUFFLING AND PARTITIONING
=========================================================

This guide covers:
1. What is Partitioning?
2. What is Shuffling?
3. How they interact
4. Performance implications
5. Practical examples
"""

from pyspark.sql import SparkSession
from pyspark.sql.functions import col, sum as spark_sum, count, rand, floor
from pyspark.sql.types import StructType, StructField, IntegerType, StringType

# Initialize Spark Session
spark = SparkSession.builder.appName("ShufflePartitionGuide").getOrCreate()

print("=" * 80)
print("PART 1: UNDERSTANDING PARTITIONING")
print("=" * 80)

# Example 1: Creating data with different partition counts
print("\n--- Example 1.1: Creating RDD with different partition counts ---")
data = range(1, 11)
rdd1 = spark.sparkContext.parallelize(data,1)
rdd2 = spark.sparkContext.parallelize(data, 4)

print(f"RDD with 1 partition: {rdd1.getNumPartitions()} partitions")
print(f"RDD with 4 partitions: {rdd2.getNumPartitions()} partitions")
print(f"Data in each partition (1 partition):")
print(f"  Partition content: {rdd1.glom().collect()}")
print(f"Data in each partition (4 partitions):")
print(f"  Partition content: {rdd2.glom().collect()}")

# Example 1.2: DataFrame partitioning
print("\n--- Example 1.2: DataFrame partitioning ---")
df = spark.createDataFrame([
    (1, "Alice", 25),
    (2, "Bob", 30),
    (3, "Charlie", 35),
    (4, "David", 28),
    (5, "Eve", 32),
    (6, "Frank", 27)
], ["id", "name", "age"])

print(f"DataFrame with default partitions: {df.rdd.getNumPartitions()}")
df_repartitioned = df.repartition(3)
print(f"DataFrame repartitioned to 3 partitions: {df_repartitioned.rdd.getNumPartitions()}")

# Show how data is distributed across partitions
print("\nData distribution across 3 partitions:")
for i in range(3):
    partition_data = df_repartitioned.rdd.mapPartitionsWithIndex(
        lambda idx, rows: rows if idx == i else []
    ).collect()
    print(f"  Partition {i}: {partition_data}")

print("\n" + "=" * 80)
print("PART 2: UNDERSTANDING SHUFFLING")
print("=" * 80)

# Example 2: Operations that trigger shuffling
print("\n--- Example 2.1: groupByKey (triggers shuffle) ---")
pairs_rdd = spark.sparkContext.parallelize([
    ("apple", 1),
    ("banana", 1),
    ("apple", 1),
    ("cherry", 1),
    ("banana", 1),
    ("apple", 1)
], numPartitions=2)

print(f"Original RDD has {pairs_rdd.getNumPartitions()} partitions")
print("Original data:", pairs_rdd.collect())

# groupByKey requires shuffling - same keys must come to same partition
grouped = pairs_rdd.groupByKey()
print(f"\nAfter groupByKey, RDD has {grouped.getNumPartitions()} partitions")
print("Grouped data:", grouped.mapValues(list).collect())
print("** Note: Shuffling happened internally to group keys together **")

# Example 2.2: reduceByKey vs groupByKey (both shuffle, different efficiency)
print("\n--- Example 2.2: reduceByKey vs groupByKey ---")
data_with_values = spark.sparkContext.parallelize([
    ("apple", 5),
    ("banana", 3),
    ("apple", 2),
    ("cherry", 8),
    ("banana", 4),
    ("apple", 1)
], numPartitions=2)

# reduceByKey - pre-aggregates before shuffle (more efficient)
reduced = data_with_values.reduceByKey(lambda x, y: x + y)
print("Using reduceByKey (efficient):")
print("  Result:", sorted(reduced.collect()))
print("  ** Data is partially aggregated BEFORE shuffling **")

# groupByKey - shuffles all values then aggregates (less efficient)
grouped_values = data_with_values.groupByKey().mapValues(sum)
print("\nUsing groupByKey + mapValues (less efficient):")
print("  Result:", sorted(grouped_values.collect()))
print("  ** All data is shuffled FIRST, then aggregated **")

print("\n--- Example 2.3: SQL operations that trigger shuffle ---")
df_sales = spark.createDataFrame([
    ("product_a", "region_1", 100),
    ("product_b", "region_2", 150),
    ("product_a", "region_2", 200),
    ("product_c", "region_1", 75),
    ("product_b", "region_1", 120),
    ("product_a", "region_1", 180)
], ["product", "region", "amount"])

print("\n1. GROUP BY (triggers shuffle):")
group_result = df_sales.groupBy("product").agg(spark_sum("amount"))
print("   Aggregating by product requires shuffling all data by product key")
print("   Result:")
print(group_result.show())

print("\n2. JOIN (triggers shuffle):")
df_products = spark.createDataFrame([
    ("product_a", "Electronics"),
    ("product_b", "Clothing"),
    ("product_c", "Food")
], ["product", "category"])

join_result = df_sales.join(df_products, "product")
print("   Joining requires shuffling to co-locate matching keys")
print("   Result:")
print(join_result.show())

print("\n" + "=" * 80)
print("PART 3: PARTITIONING STRATEGIES")
print("=" * 80)

# Example 3.1: Default partitioning (hash partitioning)
print("\n--- Example 3.1: Hash Partitioning (default) ---")
hash_df = spark.createDataFrame([
    ("id_" + str(i), "value_" + str(i % 3)) for i in range(12)
], ["id", "category"])

hash_partitioned = hash_df.repartition(4, "category")
print(f"Repartitioned by 'category' column into 4 partitions")
print("Distribution across partitions:")
for i in range(4):
    partition_data = hash_partitioned.rdd.mapPartitionsWithIndex(
        lambda idx, rows: rows if idx == i else []
    ).collect()
    print(f"  Partition {i}: {len(partition_data)} records")

# Example 3.2: Range partitioning
print("\n--- Example 3.2: Range Partitioning ---")
range_df = spark.createDataFrame([
    (i, "value_" + str(i)) for i in range(1, 21)
], ["number", "data"])

# Simulate range partitioning by bucketing
bucketed = range_df.repartition(4, col("number"))
print("Partitioned by number ranges into 4 partitions")
print("Distribution (should split by ranges):")
for i in range(4):
    partition_data = bucketed.rdd.mapPartitionsWithIndex(
        lambda idx, rows: sorted(rows, key=lambda x: x[0]) if idx == i else []
    ).collect()
    if partition_data:
        numbers = [row[0] for row in partition_data]
        print(f"  Partition {i}: numbers {min(numbers)}-{max(numbers)}")

print("\n" + "=" * 80)
print("PART 4: SHUFFLE PERFORMANCE IMPLICATIONS")
print("=" * 80)

# Example 4: Demonstrating shuffle impact
print("\n--- Example 4: Impact of unnecessary shuffles ---")
large_df = spark.createDataFrame([
    (i, i % 10, "value_" + str(i)) for i in range(10000)
], ["id", "category", "data"])

print("\nScenario 1: Multiple shuffles (INEFFICIENT)")
print("  Step 1: GROUP BY category -> SHUFFLE 1")
step1 = large_df.groupBy("category").agg(count("*").alias("count"))
print("  Step 2: GROUP BY count -> SHUFFLE 2") 
step2 = step1.groupBy("count").agg(count("*").alias("cat_count"))
print("  Result requires 2 separate shuffles")

print("\nScenario 2: Optimized (EFFICIENT)")
print("  Combine operations to reduce shuffles:")
optimized = large_df.groupBy("category").agg(count("*").alias("count"))
print("  Result with single optimized shuffle")

print("\n--- Example 5: Partition size impact ---")
print("\nSmall number of partitions (few large partitions):")
print("  ✗ Poor parallelism")
print("  ✗ Memory pressure on executor")
print("  ✗ Slower processing")
df_small_part = large_df.repartition(2)
print(f"  Data in 2 partitions: ~{10000//2} records each")

print("\nLarge number of partitions (many small partitions):")
print("  ✓ Better parallelism")
print("  ✓ Lower memory per executor")
print("  ✗ Scheduling overhead")
df_large_part = large_df.repartition(50)
print(f"  Data in 50 partitions: ~{10000//50} records each")

print("\nOptimal number of partitions:")
print("  = 2-4x number of executor cores")
print("  = partition size 128-256 MB")

print("\n" + "=" * 80)
print("PART 5: ADVANCED EXAMPLES")
print("=" * 80)

# Example 5.1: Using coalesce to reduce partitions without shuffle
print("\n--- Example 5.1: coalesce vs repartition ---")
df = spark.createDataFrame([(i, "val") for i in range(100)], ["id", "value"])
df_10_partitions = df.repartition(10)

print(f"Starting with {df_10_partitions.rdd.getNumPartitions()} partitions")

coalesced = df_10_partitions.coalesce(5)
print(f"After coalesce(5): {coalesced.rdd.getNumPartitions()} partitions")
print("  ** coalesce: NO SHUFFLE (merges adjacent partitions) **")

repartitioned = df_10_partitions.repartition(5)
print(f"After repartition(5): {repartitioned.rdd.getNumPartitions()} partitions")
print("  ** repartition: INVOLVES SHUFFLE (redistribute data) **")

# Example 5.2: Custom partitioning
print("\n--- Example 5.2: Custom partitioning by column ---")
transactions = spark.createDataFrame([
    ("2024-01-01", "user1", 100),
    ("2024-01-02", "user2", 150),
    ("2024-01-01", "user3", 200),
    ("2024-01-03", "user1", 120),
    ("2024-01-02", "user4", 180),
    ("2024-01-03", "user2", 90)
], ["date", "user", "amount"])

# Partition by date - good for time-series analytics
partitioned_by_date = transactions.repartition(3, "date")
print("Transactions partitioned by date")
print("This is efficient for queries filtering by date range")

# Example 5.3: Bucketing (pre-shuffle optimization)
print("\n--- Example 5.3: Bucketing for efficient joins ---")
df1 = spark.createDataFrame([
    ("a", 1), ("b", 2), ("c", 3), ("a", 4), ("b", 5)
], ["key", "value1"])

df2 = spark.createDataFrame([
    ("a", 10), ("b", 20), ("c", 30), ("a", 40)
], ["key", "value2"])

print("\nWithout bucketing:")
print("  JOIN requires shuffling both dataframes by 'key'")
result = df1.join(df2, "key")
print("  Result:")
print(result.show())

print("\nWith bucketing (ideal for frequent joins):")
print("  Both tables bucketed by 'key' -> join is faster")
print("  ** No shuffle needed during join **")

print("\n" + "=" * 80)
print("PART 6: BEST PRACTICES SUMMARY")
print("=" * 80)

best_practices = """
1. PARTITIONING BEST PRACTICES:
   ✓ Target 128-256 MB per partition
   ✓ Number of partitions = 2-4 × CPU cores in cluster
   ✓ Use coalesce() when reducing partitions (avoids shuffle)
   ✓ Use repartition() when increasing partitions or reordering

2. SHUFFLING BEST PRACTICES:
   ✓ Minimize shuffle operations - every shuffle is expensive
   ✓ Use reduceByKey() instead of groupByKey() when possible
   ✓ Partition data intelligently before grouping
   ✓ Use bucketing for frequently joined tables
   ✓ Cache data if using it multiple times

3. OPERATIONS THAT TRIGGER SHUFFLES:
   - groupByKey(), reduceByKey(), aggregateByKey()
   - GROUP BY, HAVING in SQL
   - JOIN operations
   - DISTINCT operations
   - repartition() (not coalesce)
   - sortByKey()

4. DEBUGGING SHUFFLES:
   - Use Spark UI to see shuffle read/write sizes
   - Watch for yellow (shuffle) stages in DAG visualization
   - High shuffle data = potential optimization opportunity
   - Skewed partitions = uneven distribution = slowness

5. PARTITION SIZING RULES OF THUMB:
   - Too few partitions: underutilized resources, memory issues
   - Too many partitions: scheduling overhead, small files
   - Sweet spot: 200 MB - 512 MB per partition
"""

print(best_practices)

print("\n" + "=" * 80)
print("READY TO RUN EXAMPLES!")
print("=" * 80)
print("""
To run these examples:
1. Save this file as 'spark_guide.py'
2. Run: spark-submit spark_guide.py
3. Check the Spark UI at http://localhost:4040 (if running locally)
4. Look for shuffle read/write metrics in the UI

Key things to observe in the Spark UI:
- Shuffle Write bytes (how much data is moved)
- Shuffle Read bytes (same data, consumed)
- Partition count and data distribution
- Task duration (skewed tasks = uneven partitioning)
""")