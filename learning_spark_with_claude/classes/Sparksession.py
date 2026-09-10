from pyspark.sql import SparkSession

class CreateSparkSession:
    def __init__(
        self,
        app_name: str = "MyApp",
        numberof_cores: int = 4,
        driver_memory: str = "2g",
        executor_memory: str = "2g",
        master: str = None
    ):
        builder = (
            SparkSession.builder
            .appName(app_name)
            .config("spark.driver.memory", driver_memory)
            .config("spark.executor.memory", executor_memory)
        )

        if master:
            builder = builder.master(master)
        else:
            builder = builder.master(f"local[{numberof_cores}]")

        self.spark = builder.getOrCreate()


