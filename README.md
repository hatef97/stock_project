
# Python Django Test
A sample microservice project with Django, Redis and Kafka to test your familiarities with these tools.

### Requirements

You need [Docker](https://docs.docker.com/get-docker/) installed on you machine to run **Redis** and **Apache Kafka** instances. [Python](https://www.python.org/downloads/) is also needed for various scripts in all the steps.

> **Note:** Preferably use Python 3.7+

### Included in the Box

Sample price data for three fictional stocks needed in the next steps are stored in `price_data.csv`. In `./redis` folder there is a docker-compose file for running a dockerized Redis database instance. Similarly, the docker-compose file for starting a dockerized instance of message queuing system Kafka is found in `./kafka` folder. This docker-compose file initializes a topic named `main_topic` after startup.

## Step 1: Price Updater Service

Write a price updater service with Python that accomplishes these tasks:

- Reads the price data in `price_data.csv` for **Stock1**, **Stock2** and **Stock3** starting from 9:00:00 to 9:59:47
- Connects to the Redis database
- For each data row, updates the time and price history of the corresponding stock 

> **Note:** Make sure Redis database is running and is accessible on `localhost` on default port `6037`

> **Hint:** The stock price history data in stored in Redis in `key`-`value` format. The key value for Stock1, Stock2 and Stock3 are `stock1`, `stock2` and `stock3` respectively. The value is in json format in which the `time` field is a list of timestamps `hhmmss`. The `price`	field is the list of stock prices at respective timestamps.

> **Hint:** Empty price entries are related to times where no data is reported for that stock

Finally, dockerize your script to be used as a standalone service.

## Step 2: Stock Performance Calculation

Now imagine we want to calculate a performance metric for each stock. This fictional performance metric is computationally very expensive and each calculation would take 3 seconds. Here, for simplicity, we simulate the calculation of this performance metric with this simple function:

```
def calculate_performance(stock_price):
	time.sleep(3)
	return 0
```
Write a python script that calculates this performance metric for stocks every minute and update the performance value in the Redis database for that stock. This value is stored in the field `performance`.  

Since this computation is heavy, we don't want to recalculate the performance metric for a stock if its price is not changed. How would you accomplish this goal? 

> **Hint:** You might want to revisit step 1 and see if it needs some changes

Now we want to go one step further and utilize parallel computing to make this task even faster. Write/Rewrite your script to use more than one core for this computation. 

Finally, dockerize your script to be used as a standalone service.

## Step 3: It's Message Queueing Time!

In this Step we want to integrate Apache Kafka in our project, so, instead of reading the data from the  `price_data.csv` file, we will be listening to a Kafka topic and get the stock price data from there. 

> **Note:** Make sure Kafka is running and is accessible on `localhost` on port `9092` and the topic `main_topic` is available.

First you need to fill the Kafka `main_topic` with the price data given in `price_data.csv`. Create a `KafkaProducer`, then read the data from  `price_data.csv` and send it to the `main_topic`.

Now that the data is saved in Kafka, repeat the task in Step 1, but use a `KafkaConsumer` to get the price data.

At this point the Price Updater service is working properly, however it is not production-ready. We want to consider HA (High Availability) and DR (Disaster Recovery) for our service. Let's assume there is a chance that our service is forcefully shut down and restarted. It is important for us to make sure that after the crash, the service starts reading data exactly from where it left off last time. Otherwise we might skip some messages or read some messages twice. 

Think about the ways you would change this service to ensure DR and implement them. 

Finally, dockerize your script to be used as a standalone service.

## Step 4: Django and DRF

The goal in this step is to create a `BuyStock` API endpoint in Django and do a basic check on the request.

Start an empty Django project and make sure `rest_framework` is installed. Create an API endpoint named `BuyStock` which accepts a **Post** request  from user. The body content is a valid json object in this form as an example:

```
{ 
	"user": "user2", 
	"stockname": "stock1", 
	"quantity" : 100 
}
```
This request needs to be verified and a proper response needs to be sent back. 
First connect to the Redis database and get the user data for this user. If the user credit is enough to buy this stock in this quantity return `Accept`, otherwise return `Deny`.

Finally, write **Integration Tests** for your API to make sure it's working correctly.

## Step 5: Requests Inception!

In this final step we want to consider an especial case based on Step 4. Let's imagine that after receiving each post request from user on `BuyStock` endpoint, we need to call an external API ourselves to verify the state of the user. The problem is that this API call might take long to respond or might even stall. Here, for simplicity, we simulate this API call with this simple function:

```
def verify_user(user_id):
	time.sleep(random.randint(1,100))
	return 0
```
The API call might take anytime between 1 to 100 second to respond. Write/Rewrite Step 4 with these considerations in mind:

- the user should immediately get notified of successful reception of their buy request, i.e. they should instantly know that we have received their request and we are working on it. 

> **Hint:** Think about Callback URLs and how they can integrate in this workflow

- Handle stalling of the external API. We will consider any duration over 60 second as stalled.

- The user should receive the result with the least amount of delay after the verification is complete.

> **Note:** Preferably make use of message queueing similar to Step 3 and utilize the microservice framework to your advantage
