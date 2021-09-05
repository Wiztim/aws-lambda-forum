import json
import boto3
from boto3.dynamodb.conditions import Key

forumDb = boto3.resource('dynamodb')
table = forumDb.Table('BoardsPostsComments')

def lambda_handler(event, context):


    data = table.query(
        IndexName="parentId-timestamp-index",
        KeyConditionExpression=Key('parentId').eq(str(0))
    )
    
    item = data["Items"]
    itemStr = json.dumps(item, default=str)
    
    html = "<html><link rel=stylesheet href=https://wiztim-forum.s3.amazonaws.com/bootstrap.min.css><body style=background-color:CDCDCD>"
    html += "<h5 style=\"position:absolute; left:2%; top:5%;\"><a href=\"https://tcze7o1n4k.execute-api.us-east-1.amazonaws.com/boards\">Forum Name</a></h5>"
    html += "<div style=\"position:absolute; left:45%; top:10%;\"><div style=text-align:center>"
    html += "<h2>Forum Name</h2><br><h3><u>Boards</u></h3><h4>"
    
    for boardTitle in item:
        html += '<a href="https://tcze7o1n4k.execute-api.us-east-1.amazonaws.com/boards/' + boardTitle['id'] + '/posts">'
        html += boardTitle['title']
        html += "</a><br>"
        
    html += "</h4></div></div></body></html>"
    
    return {
        'statusCode': 200,
        'headers': {
            'Content-Type': 'text/html',
            'Access-Control-Allow-Origin': '*'
        },
        'body': html
    }
    
