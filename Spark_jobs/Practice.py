import time
class Practice:
    def __init__(self, spark):
        self.spark = spark

    def run(self):
        df = self.spark.read.csv("data/students_en.csv", header=True)

        start = time.time()
        df.show()
        elapsed = time.time() - start
        print(f"show() time: {elapsed:.2f}s")