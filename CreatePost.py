import json
import boto3
import time
import uuid

client = boto3.client('dynamodb')

def lambda_handler(event, context):

    bodyJson = json.loads(event['body'])
    

    try:
        epochTime = int(time.time())
        boardId = event['pathParameters']['boardId']
        title = bodyJson['title']
        content = bodyJson['content']
        username = bodyJson['username']
        
        if username == "":
            username = 'Anonymous'
            
        if title == "" or content == "":
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
                    'S':str(boardId)
                },
                'type':{
                    'S':'post'  
                },
                'title':{
                    'S':str(title)
                },
                'content':{
                    'S':content
                },
                'username':{
                    'S':str(username)
                },
                'latestActivity':{
                    'N':str(epochTime)
                }
            }
        )
    except:
        return {
            'statusCode': 400,
            'body': str(sys.exc_info())
        }

    
    return {
        'statusCode': 200,
        'headers': {
            'Access-Control-Allow-Origin': '*'            
        },
        'body': str(data)
    }
