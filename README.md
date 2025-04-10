# sensor-data-streaming
A solution for Kafka streaming with MongoDB output

## Project Overview
This project demonstrates a real-time data streaming application using Apache Kafka and MongoDB. The system processes sensor data from Kafka topics, computes average values over windows of time, and stores the results in a MongoDB database. The project is written in Python using Apache Spark for stream processing and MongoDB for storage.

## Technologies Used
- **Apache Kafka**: A distributed event streaming platform for real-time data processing.
- **MongoDB**: A NoSQL database to store the processed results.
- **Python**: The programming language used for developing the streaming application.
- **Apache Spark**: A unified analytics engine used for stream processing and computation of windowed averages.

## Project Setup

### Step 1: Install MongoDB
1. Download and install MongoDB from the [official MongoDB website](https://www.mongodb.com/try/download/community).
2. Start the MongoDB service on your local machine by running `mongod.exe`.

### Step 2: Install Kafka
1. Download and install Apache Kafka from the [Apache Kafka website](https://kafka.apache.org/downloads).
2. Start Kafka in the `bin\windows` folder.

### Step 3: Install Python Dependencies
1. Make sure Python is installed on your system.
2. Install the required Python packages by running the following command:
   ```bash
   pip install kafka-python pyspark pymongo
   ```

### Step 4: Kafka Topics
The Kafka topics `sensor-input` and `sensor-output` were already created before the script was run. These topics are used as input and output channels for the sensor data and processed results.

### Step 5: Run the Python Script
1. The Python script listens to the `sensor-input` Kafka topic, processes the incoming data, and calculates the average values of sensor readings in 1-minute windows.
2. It then writes the processed data to the `sensor-output` Kafka topic and stores the results in MongoDB.

To run the Python script, navigate to your project folder and run:
```bash
python kafka_streaming.py
```
For example, your files might be located at:
```
C:\Users\NikhileshKalyankumar\OneDrive\Desktop\Assignment\fp-de-home-assignment
```

### Step 6: MongoDB Data Storage
The results of the sensor data aggregation will be stored in a MongoDB collection named `sensor_data`. You can view the stored data by running the following MongoDB commands:
1. Connect to MongoDB using `mongosh`:
   ```bash
   mongosh --host 127.0.0.1 --port 27017
   ```
2. Switch to the database where the data is stored:
   ```bash
   use sensor_data
   ```
3. View the stored data:
   ```bash
   db.sensor_data.find().pretty()
   ```

## Key Features
- **Real-time Data Processing**: The application uses Kafka for streaming and Spark for processing in real-time.
- **Data Aggregation**: The system calculates average values for each sensor over a window of 1 minute.
- **MongoDB Storage**: Processed data is stored in MongoDB for later use.

## Conclusion
This project demonstrates how to build a real-time streaming pipeline using Kafka and MongoDB, with Apache Spark handling the data aggregation. It serves as an example of integrating these technologies for processing and storing large volumes of data in a scalable and efficient manner.

## File Structure
- kafka_streaming.py: The main Python script that handles data processing and integration with Kafka and MongoDB.

