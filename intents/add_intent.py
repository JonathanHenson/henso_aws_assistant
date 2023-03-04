import json
import boto3
from jsonschema import validate, ValidationError

intent_data_schema = {
  "type": "object",
  "properties": {
    "sample_utterances": {
      "type": "array",
      "items": {
        "type": "string"
      }
    },
    "slots": {
      "type": "object",
      "additionalProperties": {
        "type": "object",
        "properties": {
          "name": {
            "type": "string"
          },
          "type": {
            "type": "string"
          },
          "prompt": {
            "type": "string"
          },
          "confirmation_prompt": {
            "type": "string"
          },
          "validation": {
            "type": "object",
            "properties": {
              "on_failure": {
                "type": "string"
              },
              "max_attempts": {
                "type": "integer"
              }
            }
          }
        }
      }
    },
    "fulfillment_activity": {
      "type": "object",
      "properties": {
        "type": {
          "type": "string",
          "enum": [
            "ReturnIntent",
            "CodeHook"
          ]
        },
        "code_hook": {
          "type": "object",
          "properties": {
            "uri": {
              "type": "string"
            },
            "message_version": {
              "type": "string"
            }
          }
        }
      }
    }
  },
  "required": [
    "sample_utterances",
    "slots",
    "fulfillment_activity"
  ]
}

dynamodb = boto3.resource('dynamodb')
lex_client = boto3.client('lex-models')

def lambda_handler(event, context):
  intent_name = event['intent_name']
  intent_data = json.loads(event['intent_data'])

  try:
    validate(instance=intent_data, schema=intent_data_schema)
    table_name = "hensosAIIntentDB"
    table = dynamodb.Table(table_name)
    item = {
        'intent_name': intent_name,
        'intent_data': intent_data
    }
    
    table.put_item(Item=item)


    lex_client.put_intent(
        name=intent_name,
        sample_uterances=intent_data['sample_uterances'],
        slots=intent_data['slots'],
        fullfillment_activity=intent_data['fullfillment_activity']
    )
    
    return {
        'statusCode': 200,
        'body': json.dumps({'message': 'Intent added successfully'})
    }

  except ValidationError as e:
    return {
      'statusCode': 400,
      'body': json.dumps({'message': str(e)})
    }

