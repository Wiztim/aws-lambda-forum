import json
import boto3
import time

client = boto3.client('dynamodb')

def lambda_handler(event, context):

    bodyJson = json.loads(event['body'])
    

    try:
        epochTime = time.time()
        title = bodyJson['title']
        id = bodyJson['id']
            
        data = client.put_item(TableName='BoardsPostsComments',
            Item = {
                'id':{
                    'S':str(id)
                },
                'timestamp':{
                    'N':str(epochTime)
                },
                'parentId':{
                    'S':str(00)
                },
                'type':{
                    'S':'board'  
                },
                'title':{
                    'S':str(title)
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
        'body': str(data)
    }
