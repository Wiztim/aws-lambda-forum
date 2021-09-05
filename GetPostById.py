import json
import boto3
from boto3.dynamodb.conditions import Key

client = boto3.resource('dynamodb')
table = client.Table('BoardsPostsComments')

def lambda_handler(event, context):

    postId = event['pathParameters']['postId']
    
    data = table.query(
        KeyConditionExpression=Key('id').eq(postId)
    )
    
    item = data["Items"]
    itemStr = json.dumps(item, default=str)

    return {
        'statusCode': 200,
        'headers': {
            'Access-Control-Allow-Origin': '*'            
        },
        'body': str(itemStr)
    }
