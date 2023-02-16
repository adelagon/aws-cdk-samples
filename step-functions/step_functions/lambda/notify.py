import json

def failure_handler(event, context):
    return {
        'statusCode': 200,
        'body': 'Parsing Failed'
    }