import json
import boto3

dynamodb = boto3.resource('dynamodb')

def lambda_handler(event, context):
    table_name = "hensosAIIntentDB"
    table = dynamodb.Table(table_name)
    
    intent_name = event['pathParameters']['intent_name']
    
    table.delete_item(Key={'intent_name': intent_name})
    
    return {
        'statusCode': 200,
        'body': json.dumps({'message': 'Intent deleted successfully'})
    }