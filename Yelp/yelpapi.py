from kafka import KafkaProducer
from yelpFusionClient import YelpFusionClient
import time
import io
import json

queryTime = 5
kafkaTopic = 'yelp'

# def CalculateAvgRating(s):
#     params = {
#         'category_filter': s
#     }
#     i = 0
#     average_rating = 0
#     total_rating = 0
#     response = client.search('San Francisco', params)
    
#     availableDataLen = len(response.businesses)

#     while( i < availableDataLen):
#         total_rating = total_rating + int(response.businesses[i].rating)
#         i = i+1

#     average_rating = total_rating / availableDataLen
    
#     return str(average_rating)


with io.open('yelpkey.json') as cred: 
    creds = json.load(cred)

    client = YelpFusionClient(creds["client_id"], creds["client_secret"])
    
    # Examples
    print(client.search('restaurant', 'san jose'))
    print(client.search('hannah-san-jose'))
    print(client.search('hannah-san-jose'))

    # producer = KafkaProducer(bootstrap_servers = 'localhost:9092')

    # while(True):
    #    producer.send(kafkaTopic, CalculateAvgRating('chinese').encode('utf-8'))
    #    producer.send(kafkaTopic, CalculateAvgRating('Indian').encode('utf-8'))
    #    producer.send(kafkaTopic, CalculateAvgRating('mediterranean').encode('utf-8'))
    #    time.sleep(queryTime)  