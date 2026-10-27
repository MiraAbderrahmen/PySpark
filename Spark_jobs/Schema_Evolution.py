
import json
from pyspark.sql import SparkSession
class SchemaEvolution:
    def __init__(self, spark):
        self.spark = spark
            
    v1_schema = {
    "type": "record",
    "name": "DeviceEvent",
    "fields": [
        {"name": "device_id", "type": "long"},
        {"name": "count", "type": "int"}
    ]
    }
    
    # Schema V2: add a new field with a default
    v2_schema = {
        "type": "record",
        "name": "DeviceEvent",
        "fields": [
            {"name": "device_id", "type": "long"},
            {"name": "count", "type": "int"},
            {
                "name": "direction",
                "type": "string",
                "default": "UNKNOWN"
            }
        ]
    }
    def produce_events(self, deployment_version):
    
            if deployment_version == 1:
                schema = SchemaEvolution.v1_schema
                events = [
                    {"device_id": 1001, "count": 250},
                    {"device_id": 1002, "count": 180},
                ]
                output = "lab_data/v1"
    
            elif deployment_version == 2:
                schema = SchemaEvolution.v2_schema
                events = [
                    {
                        "device_id": 1001,
                        "count": 260,
                        "direction": "ENTRY",
                    },
                    {
                        "device_id": 1002,
                        "count": 175,
                        "direction": "EXIT",
                    },
                ]
                output = "lab_data/v2"
    
            else:
                raise ValueError("Unknown deployment version")
            
            
            df = self.spark.createDataFrame(events)

            (
                df.write
                .format("avro")
                .option("avroSchema", json.dumps(schema))
                .mode("overwrite")
                .save(output)
            )

            print(f"Producer deployment V{deployment_version} wrote {output}")
    
    

    def run(self):
        self.produce_events(1)      
        print("\nBACKWARD: V2 reader reads V1 data")

        backward = (
            self.spark.read
            .format("avro")
            .option("avroSchema", json.dumps(SchemaEvolution.v2_schema))
            .load("lab_data/v1")
        )

        backward.show(truncate=False)