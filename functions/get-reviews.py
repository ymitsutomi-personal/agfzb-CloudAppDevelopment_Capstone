#
#
# main() will be run when you invoke this action
#
# @param Cloud Functions actions accept a single parameter, which must be a JSON object.
#
# @return The output of this action, which must be a JSON object.
#
#
from cloudant.client import Cloudant
from cloudant.result import Result, ResultByKey
from cloudant.error import CloudantException
from collections import namedtuple
import requests
import json


def main(dict):
    databaseName = "reviews"
    wk_result = []

    try:
        client = Cloudant.iam(
            account_name=dict["COUCH_USERNAME"],
            api_key=dict["IAM_API_KEY"],
            connect=True,
        )
        review_db = client[databaseName]
        
        wk_dealer_id = dict.get('dealerId')
        
        result_collection = Result(review_db.all_docs, include_docs=True)
        
        for wk_doc in result_collection:
            dummy_doc = wk_doc['doc']
            
            if dummy_doc.get('purchase_date') is not None:
                wk_element = {
                    "id": dummy_doc.get('id'),
                    "name": dummy_doc.get('name'),
                    "dealership": dummy_doc.get('dealership'),
                    "review": dummy_doc.get('review'),
                    "purchase": dummy_doc.get('purchase'),
                    "purchase_date": dummy_doc.get('purchase_date'),
                    "car_make": dummy_doc.get('car_make'),
                    "car_model": dummy_doc.get('car_model'),
                    "car_year": dummy_doc.get('car_year')
                }
            else:
                 wk_element = {
                    "id": dummy_doc.get('id'),
                    "name": dummy_doc.get('name'),
                    "dealership": dummy_doc.get('dealership'),
                    "review": dummy_doc.get('review'),
                    "purchase": dummy_doc.get('purchase'),
                }               
            
            
            if wk_dealer_id is not None:
                if int(wk_dealer_id) == wk_element.get('dealership'):
                    wk_result.append(wk_element)
            else:
                wk_result.append(wk_element)
            
        
    except CloudantException as ce:
        print("unable to connect")
        return {
            "error": {
                "statusCode": 500,
                "body": "Something went wrong on the server"
            }
        }
    except (requests.exceptions.RequestException, ConnectionResetError) as err:
        print("connection error")
        return {
            "error": {
                "statusCode": 500,
                "body": "Something went wrong on the server"
            }
        }

    if len(wk_result) == 0:
        return {
            "error": {
                "statusCode": 404,
                "body": "dealerId does not exist"
            }
        }
    else:
        return {
            "result": wk_result
        }
