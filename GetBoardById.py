import json
import boto3
from boto3.dynamodb.conditions import Key

client = boto3.resource('dynamodb')
table = client.Table('BoardsPostsComments')

def lambda_handler(event, context):

    boardId = event['pathParameters']['boardId']
    
    data = table.query(
        KeyConditionExpression=Key('id').eq(boardId)
    )
    
    item = data["Items"]
    itemStr = json.dumps(item[0], default=str)
    
    return {
        'statusCode': 200,
        'headers': {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': '*'            
        },
        'body': itemStr
    }
