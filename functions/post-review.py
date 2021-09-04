#
#
# main() will be run when you invoke this action
#
# @param Cloud Functions actions accept a single parameter, which must be a JSON object.
#
# @return The output of this action, which must be a JSON object.
#
#
import sys

def main(dict):
    
    try:
        wk_review = dict['review']
    except:
        return {
            "error": {
                "statusCode": 500,
                "body": "Something went wrong on the server"
            }
        }
    
    
    return {
        "doc": {
            "id": wk_review.get('id'),
            "name": wk_review.get('name'),
            "dealership": wk_review.get('dealership'),
            "review": wk_review.get('review'),
            "purchase": wk_review.get('purchase'),
            "purchase_date": wk_review.get('purchase_date'),
            "car_make": wk_review.get('car_make'),
            "car_model": wk_review.get('car_model'),
            "car_year": wk_review.get('car_year')
        },
        "dbname": "reviews"
  }
