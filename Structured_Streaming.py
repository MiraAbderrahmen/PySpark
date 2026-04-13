from pyspark.sql import SparkSession
from pyspark.sql.functions import col

# Create Spark session
spark = SparkSession.builder \
    .appName("KafkaStructuredStreaming") \
    .getOrCreate()

spark.sparkContext.setLogLevel("WARN")

# Read from Kafka
df = spark.readStream \
    .format("kafka") \
    .option("kafka.bootstrap.servers", "kafka:29092") \
    .option("subscribe", "test_topic") \
    .option("startingOffsets", "earliest") \
    .load()

# Convert binary key/value to string
df_string = df.select(
    col("topic"),
    col("partition"),
    col("offset"),
    col("timestamp"),
    col("key").cast("string"),
    col("value").cast("string")
)

# Print to console
query = df_string.writeStream \
    .format("console") \
    .outputMode("append") \
    .option("truncate", "false") \
    .option("checkpointLocation", "/tmp/checkpoint-test_topic") \
    .start()

query.awaitTermination()