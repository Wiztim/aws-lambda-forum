import json
import boto3
import time
import uuid


client = boto3.client('dynamodb')
lambdaClient = boto3.client('lambda')

def lambda_handler(event, context):

    bodyJson = json.loads(event['body'])
    epochTime = int(time.time())
    parentPostId = event['pathParameters']['postId']
    content = bodyJson['content']
    username = bodyJson['username']
    opTime = bodyJson['opTime']
    
    if username == "":
        username = 'Anonymous'
        
    if content == "":
        return {
            'statusCode' : 400
        }
        
    data = client.put_item(TableName='BoardsPostsComments',
        Item = {
            'id':{
                'S':str(uuid.uuid4())
            },
            'timestamp':{
                'N':str(epochTime)
            },
            'parentId':{
                'S':parentPostId
            },
            'type':{
                'S':'comment'  
            },
            'content':{
                'S':content
            },
            'username':{
                'S':username
            }
        }
    )

    try:
        client.update_item(
            TableName='BoardsPostsComments',
            Key={
                'id':{
                    'S':parentPostId
                },
                'timestamp':{
                    'N':str(opTime)
                }
            },
            UpdateExpression="SET latestActivity=:t",
            ExpressionAttributeValues={
                ':t':{
                    'N':str(epochTime)
                }
            },
            ReturnValues="UPDATED_NEW"
        )
        
    except:
        return {
            'statusCode': 400,
            'body': event
        }

    return {
        'statusCode': 200,
        'headers': {
            'Access-Control-Allow-Origin': '*'            
        },
        'body': str(data)
    }