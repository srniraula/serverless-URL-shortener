# entry point Lambda calls

from create import handle as handle_create
from redirect import handle as handle_redirect
from analytics import handle as handle_analytics

def lambda_handler(event, context):
    method = event.get('httpMethod')
    path = event.get('path','')

    if method == 'POST' and path == '/shorten':
        return handle_create(event)
    elif method == 'GET' and path.endswith('/stats'):
        return handle_analytics(event)
    elif method == 'GET':
        return handle_redirect(event)
    else:
        return {'statusCode': 404,'body': 'Not found'}
    