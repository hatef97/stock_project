import csv
from kafka import KafkaProducer

# Kafka configuration
kafka_bootstrap_servers = 'localhost:9092'
kafka_topic = 'main_topic'

# Create Kafka producer
kafka_producer = KafkaProducer(bootstrap_servers=kafka_bootstrap_servers)

# Read price data from CSV and send it to Kafka topic
with open('price_data.csv', 'r') as csv_file:
    csv_reader = csv.reader(csv_file)
    next(csv_reader)  # Skip header row

    for row in csv_reader:
        timestamp = row[0]
        stock1_price = row[1]
        stock2_price = row[2]
        stock3_price = row[3]

        # Send stock price data to Kafka topic
        kafka_producer.send(kafka_topic, key=timestamp.encode(),
                            value=f"{stock1_price},{stock2_price},{stock3_price}".encode())

# Flush and close the Kafka producer
kafka_producer.flush()
kafka_producer.close()
