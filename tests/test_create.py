import json
import pytest
import boto3
from moto import mock_aws
from unittest.mock import patch
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

@pytest.fixture
def dynamodb_table():
    with mock_aws():
        dynamodb = boto3.resource('dynamodb', region_name='eu-north-1')
        table = dynamodb.create_table(
            TableName='url-shortener',
            KeySchema=[{'AttributeName': 'shortCode', 'KeyType': 'HASH'}],
            AttributeDefinitions=[{'AttributeName': 'shortCode', 'AttributeType': 'S'}],
            BillingMode='PAY_PER_REQUEST'
        )
        yield table

@mock_aws
def test_create_returns_short_url(dynamodb_table):
    from create import handle
    event = {
        'httpMethod': 'POST',
        'path': '/shorten',
        'body': json.dumps({'url': 'https://google.com'})
    }
    response = handle(event)
    assert response['statusCode'] == 201
    body = json.loads(response['body'])
    assert 'short_url' in body

@mock_aws
def test_create_missing_url_returns_400(dynamodb_table):
    from create import handle
    event = {
        'httpMethod': 'POST',
        'path': '/shorten',
        'body': json.dumps({})
    }
    response = handle(event)
    assert response['statusCode'] == 400