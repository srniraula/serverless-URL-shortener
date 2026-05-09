import json
import pytest
import boto3
from moto import mock_aws
from datetime import datetime, timezone
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
        table.put_item(Item={
            'shortCode': 'abc123',
            'originalUrl': 'https://google.com',
            'createdAt': datetime.now(timezone.utc).isoformat(),
            'clicks': 0
        })
        yield table

@mock_aws
def test_redirect_returns_302(dynamodb_table):
    from redirect import handle
    event = {
        'httpMethod': 'GET',
        'path': '/abc123',
        'pathParameters': {'shortCode': 'abc123'}
    }
    response = handle(event)
    assert response['statusCode'] == 302
    assert response['headers']['Location'] == 'https://google.com'

@mock_aws
def test_redirect_not_found_returns_404(dynamodb_table):
    from redirect import handle
    event = {
        'httpMethod': 'GET',
        'path': '/xxxxxx',
        'pathParameters': {'shortCode': 'xxxxxx'}
    }
    response = handle(event)
    assert response['statusCode'] == 404