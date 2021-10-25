import json
import boto3
from boto3.dynamodb.conditions import Key
import time

lambdaClient = boto3.client('lambda')
client = boto3.resource('dynamodb')
table = client.Table('BoardsPostsComments')

def lambda_handler(event, context):

    lambdaResponse = lambdaClient.invoke(FunctionName = 'GetPostById', InvocationType = 'RequestResponse', Payload = json.dumps(event))
    responseJson = json.loads(lambdaResponse['Payload'].read())
    postData = json.loads(responseJson['body'])[0]

    lambdaResponse = lambdaClient.invoke(FunctionName = 'GetBoardById', InvocationType = 'RequestResponse', Payload = json.dumps(event))
    responseJson = json.loads(lambdaResponse['Payload'].read())
    boardData = json.loads(responseJson['body'])
    
    postId = event['pathParameters']['postId']
    
    data = table.query(
        IndexName="parentId-timestamp-index",
        KeyConditionExpression=Key('parentId').eq(postId)
    )
    
    commentArr = data["Items"]
    
    html = "<html><link rel=stylesheet href=https://wiztim-forum.s3.amazonaws.com/bootstrap.min.css><body style=background-color:CDCDCD>"
    html += "<h5 style=\"position:absolute; left:2%; top:5%;\"><a href=https://github.com/Wiztim/aws-lambda-forum target=\"_blank\" rel=\"noopener noreferrer\">GitHub Repo</a><br><a href=\"/boards\">Phoenix Forum</a> > <a href=\"/boards/" + boardData['id'] + "/posts\">" + boardData['title'] + "</a> > " + postData['title'] + "</h5>"
    html += "<div style=\"position:absolute; left:10%; top:10%;\">"
    html += "<br><h3>" + postData['title'] + "</h3>"
    
    html += "<button style=background-color:BDFFBD type=button id=createPost>Reply to post</button>"
    html += "<script type=\"text/javascript\">document.getElementById(\"createPost\").onclick = function() {if(document.getElementById(\"createPost\").innerHTML === \'Reply to post\'){document.getElementById(\"postForm\").style.display = \"block\";document.getElementById(\"createPost\").innerHTML = \'Close Post Form\';}else{document.getElementById(\"postForm\").style.display = \"none\";document.getElementById(\"createPost\").innerHTML = \'Reply to post\';}}</script>"
    html += "<div style=display:none id=postForm>Body: <textarea id=bodyInput></textarea><br>Username: <input type=text id=nameInput style=\"position:absolute;\"></input><br>"
    html += "<button type=button id=submitPost>Submit Post</button>"
    html += "<script type=text/javascript>document.getElementById(\"submitPost\").onclick = async function() {let postData = {\"content\":bodyInput.value,\"username\":nameInput.value};postData = JSON.stringify(postData); await fetch(\"https://tcze7o1n4k.execute-api.us-east-1.amazonaws.com/boards/" + boardData['id'] + "/posts/" + postData['id'] + "/comments\", {method:\"POST\", body:postData}); location.reload();return false;}</script></div>"

    postTime = time.strftime('%m-%d-%Y at %H:%M:%S (UTC)', time.localtime(int(postData['timestamp'])))
    html += '<div style=\"border:3px; border-style:solid; width:80vw\"><u>' + postData['username'] + '</u><br>'
    html += postData['content'] + "<div style=\"text-align:right; position:relative; right:1%\">Posted on: " + postTime + "</div></div>"
    
    for commentData in commentArr:
        commentTime = time.strftime('%m-%d-%Y at %H:%M:%S (UTC)', time.localtime(commentData['timestamp']))
        html += '<div style=\"border:3px; border-style:solid; width:80vw\"><u>' + commentData['username'] + '</u><br>'
        html += commentData['content'] + "<div style=\"text-align:right; position:relative; right:1%\">Posted on: " + commentTime + "</div></div>"
        
    html += "</div></body></html>"

        
    return {
        'statusCode': 200,
        'headers': {
            'Content-Type': 'text/html',
            'Access-Control-Allow-Origin': '*'            
        },
        'body': html
    }
