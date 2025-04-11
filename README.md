# sensor-data-streaming
A solution for Real-Time Sensor Data Processing

## Project Overview
This project demonstrates a real-time data streaming application using Apache Saprk. The system processes sensor data from Kafka topics, computes average values over windows of time, and stores the results in a MongoDB database. The project is written in Python using Apache Spark for stream processing and MongoDB for storage.

## Technologies Used
- **Docker**: Used to run Kafka services.
- **Python**: The programming language used for developing the streaming application.
- **Apache Spark**: A unified analytics engine used for stream processing and computation of windowed averages.
- **MongoDB**: A NoSQL database to store the processed results.
- **VS Code**: The IDE used for writing and managing the code.

## Project Setup

### Step 1: Install Python
1. Download and install **Python** from the [official Python website](https://www.python.org/downloads/).
2. Ensured that **pip** (the Python package manager) is installed along with Python.

### Step 2: Install Apache Spark
1. Download and install **Apache Spark** from the [Apache Spark website](https://spark.apache.org/downloads.html).
2. Follow the instructions to set up **Spark** on your local machine.

### Step 3: Install Docker Desktop
1. Install **Docker Desktop** from the [official Docker website](https://www.docker.com/products/docker-desktop).
2. Once installed, run Docker Desktop to set up the environment for Kafka.
3. Download the assignment zip folder, open it in Docker, and start the Kafka producer and topic broker from there.
   
### Step 4: Install MongoDB
1. Download **MongoDB** from the [official MongoDB website](https://www.mongodb.com/try/download/community).
2. Install and set up **MongoDB** on your machine.
3. **Start MongoDB** by running `mongod.exe` on your system to initiate the database.

### Step 5: Install Python Dependencies
Make sure the following Python packages are installed:
```bash
pip install kafka-python pyspark pymongo
```
### Step 6: Kafka Topics
The Kafka topics `sensor-input` and `sensor-output` were already created before the script was run. These topics are used as input and output channels for the sensor data and processed results.

### Step 7: Run the Python Script
1. The Python script listens to the `sensor-input` Kafka topic, processes the incoming data, and calculates the average values of sensor readings in 1-minute windows.
2. It then writes the processed data to the `sensor-output` Kafka topic and stores the results in MongoDB.

To run the Python script, navigate to your project folder and run:
```bash
python kafka_streaming.py
```
For example, your files might be located at:
```
C:\Users\NK\OneDrive\Desktop\Assignment\fp-de-home-assignment
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

