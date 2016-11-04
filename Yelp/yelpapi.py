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
    while(true):
       producer.send(kafkaTopic, CalculateAvgRating('chinese').encode('utf-8'))
       producer.send(kafkaTopic, CalculateAvgRating('Indian').encode('utf-8'))
       producer.send(kafkaTopic, CalculateAvgRating('mediterranean').encode('utf-8'))
       time.sleep(queryTime)  

def CalculateAvgRating(cuisine):
    params = {
        'category_filter': cuisine
    }
    i = 0
    average_rating = 0
    total_rating = 0
    response = client.search('San Francisco', **params)
    while( i < int(response.total) ):
        total_rating = total_rating + int(response.businesses[i]. rating)
        i = i+1
    average_rating = total_rating/int(response.total)
    return average_rating
    
