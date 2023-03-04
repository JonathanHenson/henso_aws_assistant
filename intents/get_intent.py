import json
import boto3

dynamodb = boto3.resource('dynamodb')

def lambda_handler(event, context):
    table_name = "hensosAIIntentDB"
    table = dynamodb.Table(table_name)
    
    intent_name = event['pathParameters']['intent_name']
    
    response = table.get_item(Key={'intent_name': intent_name})
    
    if 'Item' not in response:
        return {
            'statusCode': 404,
            'body': json.dumps({'message': 'Intent not found'})
        }
    
    item = response['Item']
    intent_data = item['intent_data']
    
    return {
        'statusCode': 200,
        'body': intent_data
    }
