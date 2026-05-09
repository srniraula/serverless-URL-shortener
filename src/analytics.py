# When owner calls with /stats, this handle() function is triggered for stats report.
import json
from db import get_url

def handle(event):
    short_code = event.get('pathParameters', {}).get('shortCode')

    if not short_code:
        return {'statusCode': 400, 'body': json.dumps({'error': 'missing short code'})}

    item = get_url(short_code)

    if not item:
        return {'statusCode': 404, 'body': json.dumps({'error': 'URL not found'})}

    return {
        'statusCode':200,
        'body': json.dumps({
            'shortCode': item['shortCode'],
            'originalUrl': item['originalUrl'],
            'createdAt': item['createdAt'],
            'clicks': int(item['clicks'])
        })
    }