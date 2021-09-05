import json
import boto3
import time
import uuid

client = boto3.client('dynamodb')

def lambda_handler(event, context):

    try:
        print("Hello World 2.")
        bodyJson = json.loads(event['body'])
        epochTime = int(time.time())
        parentPostId = event['pathParameters']['postId']
        content = bodyJson['content']
        username = bodyJson['username']
        
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
                    'S':str(parentPostId)
                },
                'type':{
                    'S':'comment'  
                },
                'content':{
                    'S':content
                },
                'username':{
                    'S':str(username)
                }
            }
        )
        
        updatePostActivity(parentPostId, epochTime)
        
    except:
        print(sys.exc_info())
        return {
            'statusCode': 400,
            'body': str(sys.exc_info())
        }

    print("End world")
    return {
        'statusCode': 200,
        'headers': {
            'Access-Control-Allow-Origin': '*'            
        },
        'body': str(data)
    }