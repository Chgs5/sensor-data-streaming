import os
import json
from kafka import KafkaProducer
from pyspark.sql import SparkSession
from pyspark.sql.functions import from_json, col, window, avg
from pyspark.sql.types import StructType, StringType, DoubleType, LongType
from pymongo import MongoClient

# Connection Setup for MongoDB
client = MongoClient("mongodb://127.0.0.1:27017")
db = client["sensor_data_db"]  # This is to create or use existing database
collection = db["sensor_readings"]  # This is to create or use existing collection

# Disable native Hadoop I/O to prevent crash on Windows
os.environ["HADOOP_OPTS"] = "-Djava.library.path="

# Kafka output producer setup
producer = KafkaProducer(
    bootstrap_servers="localhost:9092",
    value_serializer=lambda v: json.dumps(v).encode("utf-8")
)

# Define the schema for incoming JSON msgs
schema = StructType() \
    .add("sensorId", StringType()) \
    .add("value", DoubleType()) \
    .add("timestamp", LongType())

# Function to write aggregated output to Kafka and MongoDB
def write_to_kafka_and_mongo(df, epoch_id):
    records = df.collect()
    for row in records:
        msg = {
            "sensorId": row["sensorId"],
            "windowStart": int(row["window"].start.timestamp() * 1000),
            "windowEnd": int(row["window"].end.timestamp() * 1000),
            "averageValue": row["avg(value)"]
        }
        # Sendind data to Kafka
        print(f"Sending to Kafka: {msg}")
        producer.send("sensor-output", msg)
        
        # Insert the same data into MongoDB database
        mongo_data = {
            "sensorId": row["sensorId"],
            "windowStart": int(row["window"].start.timestamp() * 1000),
            "windowEnd": int(row["window"].end.timestamp() * 1000),
            "averageValue": row["avg(value)"]
        }
        collection.insert_one(mongo_data)  # Insert into MongoDB
        print(f"Inserted into MongoDB: {mongo_data}")

# To start Spark Session
spark = SparkSession.builder \
    .appName("SensorAverageAggregator") \
    .master("local[*]") \
    .config("spark.jars.packages", "org.apache.spark:spark-sql-kafka-0-10_2.12:3.5.0") \
    .getOrCreate()

spark.sparkContext.setLogLevel("WARN")

# To read streaming data from Kafka
df_raw = spark.readStream \
    .format("kafka") \
    .option("kafka.bootstrap.servers", "localhost:9092") \
    .option("subscribe", "sensor-input") \
    .option("startingOffsets", "latest") \
    .load()

# Parse Kafka 'value' column from binary to JSON
df_json = df_raw.selectExpr("CAST(value AS STRING)") \
    .select(from_json(col("value"), schema).alias("data")) \
    .select("data.*")

# Add proper event time column from timestamp
df_with_timestamp = df_json.withColumn("eventTime", (col("timestamp") / 1000).cast("timestamp"))

# To Perform windowed average aggregation
aggregated = df_with_timestamp \
    .withWatermark("eventTime", "1 minute") \
    .groupBy(
        window(col("eventTime"), "1 minute"),
        col("sensorId")
    ).agg(avg("value"))

# Write the result back to Kafka and MongoDB using foreachBatch
query = aggregated.writeStream \
    .foreachBatch(write_to_kafka_and_mongo) \
    .option("checkpointLocation", "C:/checkpoint") \
    .outputMode("update") \
    .start()

query.awaitTermination()
