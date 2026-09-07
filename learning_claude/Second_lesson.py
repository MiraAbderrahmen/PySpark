# Here we learn about sparkSession
from pyspark.sql import SparkSession


spark=SparkSession.builder.appName("sparkSessionExample").getOrCreate()


data=[("John", 28), ("Jane", 32), ("Mike", 25), ("Emily", 30)]


sparkdf=spark.createDataFrame(data,["name","age"])


sparkcsv=spark.read.csv("data/students_en.csv",header=True)




sparkcsv.select("age","name").show()

print("student older than 27 are :")
sparkcsv.filter(sparkcsv.age>=27).show()

print("number of the students are :")
print(sparkcsv.count())



print("number of students with score > 85 are :")
print(sparkcsv.filter(sparkcsv.score>85).count())


