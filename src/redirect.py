# Handles GET /{shortCode}
# When user hits shortened url in their browser, our API gateway
# recives that HTTP GET request, then forwards to lambda
# which calls this handler which gets original URL and returns 
# a HTTP 302 response with original URL.
import json
from db import get_url, increment_clicks

def handle(event):
    short_code = event.get('pathParameters', {}).get('shortCode')

    if not short_code:
        return {
            'statusCode': 400, 
            'body': json.dumps({'error': 'missing short code'})
            }
    item = get_url(short_code)

    if not item:
        return {
            'statusCode': 404, 
            'body': json.dumps({'error': 'URL not found'})
            }
    
    increment_clicks(short_code)

    return {
        'statusCode':302,
        'headers': {'Location': item['originalUrl']},
        'body':''
    }


