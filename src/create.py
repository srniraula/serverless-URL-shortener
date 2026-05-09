# handles POST /shorten
# When api gateway receives POST request, it forwards to lambda, which calls
# this handle() function. It creates shortCode, stores in DynamoDB,
# and returns to the user the shortened url.

# It Generate the code, capture the current UTC timestamp as 
# an ISO string (e.g. 2026-05-09T10:00:00+00:00), and write both to DynamoDB.


import json
from datetime import datetime,timezone
from db import save_url
from utils import generate_short_code

BASE_URL = 'https://hcjkl5ahwl.execute-api.eu-north-1.amazonaws.com/prod'

def handle(event):
    # It returns value of 'body' key from Lambda event and converts from a JSON string to a python dictionary
    body = json.loads(event.get('body','{}'))
    original_url = body.get('url')

    if not original_url:
        return {
            'statusCode':400, # status code 400 is for bad request -> client side problem
            'body': json.dumps({'error': 'url is required'})
        }
    
    short_code = generate_short_code()
    # timezone.utc returns time that is UTC, isoformat() returns time in iso 8601 formatted string
    created_at = datetime.now(timezone.utc).isoformat()
    save_url(short_code, original_url, created_at)

    return {
        'statusCode': 201, # Created response
        # It returns a newly created shortened URL to send back to the client.
        'body': json.dumps({'short_url': f'{BASE_URL}/{short_code}'})
    }