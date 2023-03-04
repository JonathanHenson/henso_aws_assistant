import boto3
import json

lex_client = boto3.client('lex-models')
dynamodb = boto3.resource('dynamodb')

def lambda_handler(event, context):
  table_name = 'hensosAIIntentDB'
  table = dynamodb.Table(table_name)

  bot_name = event['bot_name']

  # Get all intents from the intent database
  response = table.scan()
  items = response.get('Items', [])

  for item in items:
    intent_name = item['intent_name']
    intent_data = json.loads(item['intent_data'])

    # Create the intent in the Lex bot
    lex_client.put_intent(
      name=intent_name,
      sampleUtterances=intent_data['sample_utterances'],
      slots=intent_data['slots'],
      fulfillmentActivity=intent_data['fulfillment_activity'],      
    )

  return {
    'statusCode': 200,
    'body': 'Intents added to bot: {}'.format(bot_name)
  }
