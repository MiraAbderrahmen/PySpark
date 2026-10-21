from pyspark.sql import SparkSession

spark = SparkSession.builder.appName("training").getOrCreate()
spark.conf.set("spark.sql.shuffle.partitions", 4)
spark.conf.set("spark.sql.adaptive.enabled", "false")
data = [
    ("Alice", "FR", 100,"payment"),
    ("Bob", "FR", 200,"cash"),
    ("Alice", "DE", 50,"card"),
    ("Bob", "DE", 300,"rental"),
    ("Charlie", "FR", 120,"lesson"),
    ("issam","Algeria", 150,"ticket"),
    ("Diana", "UK", 180,"payment"),
    ("Eve", "FR", 250,"cash"),
    ("Frank", "DE", 95,"rental"),
    ("Grace", "UK", 210,"card"),
    ("Henry", "Algeria", 160,"lesson"),
    ("Iris", "FR", 140,"ticket"),
    ("Jack", "DE", 275,"payment"),
    ("Kate", "UK", 320,"cash"),
    ("Liam", "Algeria", 110,"card"),
    ("Mona", "FR", 190,"rental"),
    ("Noah", "DE", 305,"lesson"),
    ("Olivia", "UK", 155,"payment"),
    ("Peter", "Algeria", 225,"ticket"),
    ("Quinn", "FR", 175,"cash")
]
df = spark.createDataFrame(data, ["name", "country", "amount", "product"])

result = (
    df.filter(df.amount > 100)
      .groupBy("country","product")
      .sum("amount")
)
result.show()
result.explain(True)