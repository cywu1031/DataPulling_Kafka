from yelp.client import Client
from yelp.oauth1_authenticator import Oauth1Authenticator
from kafka import KafkaProducer
import time
import io
import json

queryTime = 5
kafkaTopic = 'yelp'

with io.open('yelpkey.json') as cred: 
    creds = json.load(cred)
    
    auth = Oauth1Authenticator(
        consumer_key = creds['consumer_key'],
        consumer_secret = creds['consumer_secret'],
        token = creds['token'],
        token_secret = creds['token_secret']
    )
    
    client = Client(auth)

    producer = KafkaProducer(bootstrap_servers = 'localhost:9092')

    params = {
        # 'term': 'pizza',
        'category_filter': 'pizza'
    }

    while(True):
        # search example
    	response = client.search('san jose', **params)

    	producer.send(kafkaTopic, response.businesses[2].name.encode('utf-8'))

    	time.sleep(queryTime)
