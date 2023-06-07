import csv
import redis

from kafka import KafkaConsumer, KafkaProducer

# Kafka configuration
kafka_bootstrap_servers = 'localhost:9092'
kafka_topic = 'main_topic'

# Create Kafka producer
kafka_producer = KafkaProducer(bootstrap_servers=kafka_bootstrap_servers)

# Read price data from CSV and send it to Kafka topic
with open('data/price_data.csv', 'r') as csv_file:
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
# Create Kafka consumer
kafka_consumer = KafkaConsumer(kafka_topic, bootstrap_servers=kafka_bootstrap_servers)

# Connect to Redis
redis_host = 'localhost'
redis_port = 6379
redis_client = redis.Redis(host=redis_host, port=redis_port)

# Process messages from Kafka topic
for message in kafka_consumer:
    key = message.key.decode()
    value = message.value.decode().split(',')

    timestamp = key
    stock1_price = value[0]
    stock2_price = value[1]
    stock3_price = value[2]

    # Update Stock1 price history
    stock1_key = 'stock1'
    stock1_data = redis_client.hgetall(stock1_key)
    if stock1_data:
        stock1_data = {k.decode(): v.decode() for k, v in stock1_data.items()}
        stock1_data['time'].append(timestamp)
        stock1_data['price'].append(stock1_price)
    else:
        stock1_data = {'time': [timestamp], 'price': [stock1_price]}
    redis_client.hmset(stock1_key, stock1_data)

    # Update Stock2 price history (similar to Stock1)
    stock2_key = 'stock2'
    stock2_data = redis_client.hgetall(stock2_key)
    if stock2_data:
        stock2_data = {k.decode(): v.decode() for k, v in stock2_data.items()}
        stock2_data['time'].append(timestamp)
        stock2_data['price'].append(stock2_price)
    else:
        stock2_data = {'time': [timestamp], 'price': [stock2_price]}
    redis_client.hmset(stock2_key, stock2_data)

    # Update Stock3 price history (similar to Stock1)
    stock3_key = 'stock3'
    stock3_data = redis_client.hgetall(stock3_key)
    if stock3_data:
        stock3_data = {k.decode(): v.decode() for k, v in stock3_data.items()}
        stock3_data['time'].append(timestamp)
        stock3_data['price'].append(stock3_price)
    else:
        stock3_data = {'time': [timestamp], 'price': [stock3_price]}
    redis_client.hmset(stock3_key, stock3_data)
