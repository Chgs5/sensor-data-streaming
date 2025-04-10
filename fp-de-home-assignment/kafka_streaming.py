from pyspark.sql import SparkSession
from pyspark.sql.functions import from_json, col, window, avg
from pyspark.sql.types import StructType, StringType, DoubleType, LongType
import json
from kafka import KafkaProducer
from pyspark.sql import SparkSession

spark = SparkSession.builder.getOrCreate()
print("Apache Spark Version:", spark.version)
# Define schema for input JSON
schema = StructType() \
    .add("sensorId", StringType()) \
    .add("value", DoubleType()) \
    .add("timestamp", LongType())

# Kafka output producer setup
producer = KafkaProducer(
    bootstrap_servers="localhost:9092",
    value_serializer=lambda v: json.dumps(v).encode("utf-8")
)

# Function to write each micro-batch to Kafka
def write_to_kafka(df, epoch_id):
    records = df.collect()
    for row in records:
        msg = {
            "sensorId": row["sensorId"],
            "windowStart": int(row["window"].start.timestamp() * 1000),
            "windowEnd": int(row["window"].end.timestamp() * 1000),
            "averageValue": row["avg(value)"]
        }
        print(f"Sending to Kafka: {msg}")
        producer.send("sensor-output", msg)

# Initialize Spark Session
spark = SparkSession.builder \
    .appName("SensorAverageAggregator") \
    .master("local[*]") \
    .config("spark.jars.packages", "org.apache.spark:spark-sql-kafka-0-10_2.12:3.5.0") \
    .getOrCreate()

spark.sparkContext.setLogLevel("WARN")

# Read sensor data from Kafka topic 'sensor-input'
df_raw = spark.readStream \
    .format("kafka") \
    .option("kafka.bootstrap.servers", "localhost:9092") \
    .option("subscribe", "sensor-input") \
    .option("startingOffsets", "latest") \
    .load()

# Convert binary value to structured JSON
df_json = df_raw.selectExpr("CAST(value AS STRING)") \
    .select(from_json(col("value"), schema).alias("data")) \
    .select("data.*")

# Convert timestamp in ms to timestamp type
df_with_timestamp = df_json.withColumn("eventTime", (col("timestamp") / 1000).cast("timestamp"))

# Windowed aggregation (1-minute tumbling window)
aggregated = df_with_timestamp \
    .withWatermark("eventTime", "1 minute") \
    .groupBy(
        window(col("eventTime"), "1 minute"),
        col("sensorId")
    ).agg(avg("value"))

# Write aggregated results to Kafka topic 'sensor-output'
query = aggregated.writeStream \
    .foreachBatch(write_to_kafka) \
    .outputMode("update") \
    .start()


# Wait until terminated
query.awaitTermination()
