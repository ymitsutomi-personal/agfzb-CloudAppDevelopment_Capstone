import requests
import json
import urllib.parse
import traceback
# import related models here
from . import models
from .models import CarDealer
from requests.auth import HTTPBasicAuth


# Create a `get_request` to make HTTP GET requests
# e.g., response = requests.get(url, params=params, headers={'Content-Type': 'application/json'},
#                                     auth=HTTPBasicAuth('apikey', api_key))
def get_request(url, **kwargs):
    print(kwargs)
    print("GET from {} ".format(url))

    try:
        # Call get method of requests library with URL and parameters
        response = requests.get(url, headers={'Content-Type': 'application/json'}, params=kwargs)
        
    except:
        # If any error occurs
        traceback.print_exc()
        print("Network exception occurred")

    status_code = response.status_code
    print("With status {} ".format(status_code))
    json_data = json.loads(response.text)
    return json_data


# Create a `post_request` to make HTTP POST requests
# e.g., response = requests.post(url, params=kwargs, json=payload)
def post_request(url, json_payload, **kwargs):
    json_obj = json_payload["review"]
    print(kwargs)
    json_str = json.dumps(json_obj)
    try:
        response = requests.post(url, json=json_obj, params=kwargs)
    except:
        print("Something went wrong")

    return response

# Create a get_dealers_from_cf method to get dealers from a cloud function
# def get_dealers_from_cf(url, **kwargs):
# - Call get_request() with specified arguments
# - Parse JSON results into a CarDealer object list
def get_dealers_from_cf(url, **kwargs):
    results = []
    # Call get_request with a URL parameter
    json_result = get_request(url)
    if json_result:
        # Get the row list in JSON as dealers
        dealers = json_result["body"]
        # For each dealer object
        for dealer in dealers:
            # Get its content in `doc` object
            dealer_doc = dealer
            # Create a CarDealer object with values in `doc` object
            dealer_obj = CarDealer(address=dealer_doc["address"], city=dealer_doc["city"], full_name=dealer_doc["full_name"],
                                   id=dealer_doc["id"], lat=dealer_doc["lat"], long=dealer_doc["long"],
                                   short_name=dealer_doc["short_name"],
                                   st=dealer_doc["st"], zip=dealer_doc["zip"])
            results.append(dealer_obj)

    return results



# Create a get_dealer_reviews_from_cf method to get reviews by dealer id from a cloud function
def get_dealer_reviews_from_cf(url, dealerId):
    results = []
    json_result = get_request(url, dealerId=dealerId)
    if 'result' in json_result:
        print(json_result)
        reviews = json_result['result']
        for review in reviews:
            try:
                review_obj = models.DealerReview(name = review["name"], 
                dealership = review["dealership"], review = review["review"], purchase=review["purchase"],
                purchase_date = review["purchase_date"], car_make = review['car_make'],
                car_model = review['car_model'], car_year= review['car_year'], sentiment= "none")
            except:
                review_obj = models.DealerReview(name = review["name"], 
                dealership = review["dealership"], review = review["review"], purchase=review["purchase"],
                purchase_date = 'none', car_make = 'none',
                car_model = 'none', car_year= 'none', sentiment= "none")
                
            review_obj.sentiment = analyze_review_sentiments(review_obj.review)
            print(review_obj.sentiment)
                    
            results.append(review_obj)

    return results



# def get_dealer_by_id_from_cf(url, dealerId):
# - Call get_request() with specified arguments
# - Parse JSON results into a DealerView object list


# Create an `analyze_review_sentiments` method to call Watson NLU and analyze text
# def analyze_review_sentiments(text):
# - Call get_request() with specified arguments
# - Get the returned sentiment label such as Positive or Negative
def analyze_review_sentiments(text):
    api_key = "fSoHbKSPd5WpkpQBbQJna2yF-kzQxAQOMfOhxJTWfxKz"
    url = "https://api.us-south.natural-language-understanding.watson.cloud.ibm.com/instances/09b9f7bf-815a-413b-ad4a-cfc725892a45/v1/analyze"

    params = dict()
    params["text"] = urllib.parse.quote(text)
    params["version"] = "2021-08-01"
    params["features"] = "sentiment"
    params["return_analyzed_text"] = "true"
    response = requests.get(url, params=params, headers={'Content-Type': 'application/json'},
                                    auth=HTTPBasicAuth('apikey', api_key))

    print(response.text)
    json_data = json.loads(response.text)
    sentiment_score = str(json_data["sentiment"]["document"]["score"])
    sentiment_label = json_data["sentiment"]["document"]["label"]
    
    return sentiment_label
