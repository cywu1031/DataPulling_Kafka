import json
import requests
from urllib.error import HTTPError
from urllib.parse import quote
from urllib.parse import urlencode

class YelpFusionClient:
    #From example provided on Yelp Github
    __API_HOST = 'https://api.yelp.com'
    __SEARCH_PATH = '/v3/businesses/search'
    __BUSINESS_PATH = '/v3/businesses/'  # Business ID will come after slash.
    __TOKEN_PATH = '/oauth2/token'
    __GRANT_TYPE = 'client_credentials'
    
    __CLIENT_ID = None
    __CLIENT_SECRET = None

    def __init__(self, cid, csecret):
        self.__CLIENT_ID = cid
        self.__CLIENT_SECRET = csecret
        
    def __obtain_bearer_token(self, host, path): 
        """Given a bearer token, send a GET request to the API.
        Args:
            host (str): The domain host of the API.
            path (str): The path of the API after the domain.
            url_params (dict): An optional set of query parameters in the request.
        Returns:
            str: OAuth bearer token, obtained using client_id and client_secret.
        Raises:
            HTTPError: An error occurs from the HTTP request.
        """
        url = '{0}{1}'.format(host, quote(path.encode('utf8')))
        assert self.__CLIENT_ID, "Please supply your client_id."
        assert self.__CLIENT_SECRET, "Please supply your client_secret."
        data = urlencode({
            'client_id': self.__CLIENT_ID,
            'client_secret': self.__CLIENT_SECRET,
            'grant_type': self.__GRANT_TYPE,
        })
        headers = {
            'content-type': 'application/x-www-form-urlencoded',
        }
        response = requests.request('POST', url, data=data, headers=headers)
        bearer_token = response.json()['access_token']
        return bearer_token

    def __request(self, host, path, bearer_token, url_params = None):
        """Given a bearer token, send a GET request to the API.
        Args:
            host (str): The domain host of the API.
            path (str): The path of the API after the domain.
            bearer_token (str): OAuth bearer token, obtained using client_id and client_secret.
            url_params (dict): An optional set of query parameters in the request.
        Returns:
            dict: The JSON response from the request.
        Raises:
            HTTPError: An error occurs from the HTTP request.
        """
        url_params = url_params or {}
        url = '{0}{1}'.format(host, quote(path.encode('utf8')))
        headers = {
            'Authorization': 'Bearer %s' % bearer_token,
        }

        print(u'Querying {0} ...'.format(url))

        response = requests.request('GET', url, headers=headers, params=url_params)

        return response.json()


    def search(self, term, location, limit = 3):
        """Query the Search API by a search term and location.
        Args:
            term (str): The search term passed to the API.
            location (str): The search location passed to the API.
        Returns:
            dict: The JSON response from the request.
        """
        bearer_token = self.__obtain_bearer_token(self.__API_HOST, self.__TOKEN_PATH)

        url_params = {
            'term': term.replace(' ', '+'),
            'location': location.replace(' ', '+'),
            'limit': limit
        }

        return self.__request(self.__API_HOST, self.__SEARCH_PATH, bearer_token, url_params=url_params)


    def get_business(self, business_id):
        """Query the Business API by a business ID.
        Args:
            business_id (str): The ID of the business to query.
        Returns:
            dict: The JSON response from the request.
        """
        bearer_token = self.__obtain_bearer_token(self.__API_HOST, self.__TOKEN_PATH)

        business_path = self.__BUSINESS_PATH + business_id

        return self.__request(self.__API_HOST, business_path, bearer_token)


    def get_reviews(self, business_id):
        bearer_token = self.__obtain_bearer_token(self.__API_HOST, self.__TOKEN_PATH)

        REVIEW_PATH = self.__BUSINESS_PATH + business_id + '/reviews'
        
        return self.__request(self.__API_HOST, REVIEW_PATH, bearer_token)