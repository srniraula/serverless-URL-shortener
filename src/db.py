# dynamodb helpers

import boto3
import os

TABLE_NAME = os.environ.get('TABLE_NAME', 'url-shortener')
REGION = os.environ.get('AWS_DEFAULT_REGION', 'eu-north-1')

def get_table():
    dynamodb = boto3.resource('dynamodb', region_name=REGION)
    return dynamodb.Table(TABLE_NAME)

def save_url(short_code, original_url, created_at):
    table = get_table()
    table.put_item(Item={
        'shortCode': short_code,
        'originalUrl': original_url,
        'createdAt': created_at,
        'clicks':0
    })

def get_url(short_code):
    table = get_table()
    resp = table.get_item(Key={'shortCode': short_code})
    return resp.get('Item')

def increment_clicks(short_code):
    table = get_table()
    table.update_item(
        Key={'shortCode': short_code},
        UpdateExpression='Add clicks :inc',
        ExpressionAttributeValues={':inc':1}
    )

