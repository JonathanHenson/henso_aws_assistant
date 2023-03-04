import json
import boto3

dynamodb = boto3.resource('dynamodb')

def lambda_handler(event, context):
    table_name = "hensosAIIntentDB"
    table = dynamodb.Table(table_name)
    
    response = table.scan()
    
    items = response['Items']
    intent_data_list = [item['intent_data'] for item in items]
    
    return {
        'statusCode': 200,
        'body': json.dumps(intent_data_list)
    }
