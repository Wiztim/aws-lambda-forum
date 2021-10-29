import json
import boto3
from boto3.dynamodb.conditions import Key
import time

lambdaClient = boto3.client('lambda')
client = boto3.resource('dynamodb')
table = client.Table('BoardsPostsComments')
cloudwatch = boto3.client('cloudwatch')

def lambda_handler(event, context):

    startTime = time.time()
    lambdaResponse = lambdaClient.invoke(FunctionName = 'GetBoardById', InvocationType = 'RequestResponse', Payload = json.dumps(event))
    responseJson = json.loads(lambdaResponse['Payload'].read())
    boardData = json.loads(responseJson['body'])

    boardId = event['pathParameters']['boardId']
    
    data = table.query(
        IndexName="parentId-timestamp-index",
        KeyConditionExpression=Key('parentId').eq(boardId)
    )
    
    postArr = data["Items"]
    
    
    html = "<html><link rel=stylesheet href=https://wiztim-forum.s3.amazonaws.com/bootstrap.min.css><body style=background-color:CDCDCD>"
    html += "<h5 style=\"position:absolute; left:2%; top:5%;\"><a href=https://github.com/Wiztim/aws-lambda-forum target=\"_blank\" rel=\"noopener noreferrer\">GitHub Repo</a><br><a href=\"/boards\">Phoenix Forum</a> > " + boardData['title'] + "</h5>"
    html += "<div style=\"position:absolute; left:10%; top:10%;\">"
    html += "<br><h3>" + boardData['title'] + "</h3>"
    html += "<button style=background-color:BDFFBD type=button id=createPost>Create Post</button>"
    html += "<script type=\"text/javascript\">document.getElementById(\"createPost\").onclick = function() {if(document.getElementById(\"createPost\").innerHTML === \'Create Post\'){document.getElementById(\"postForm\").style.display = \"block\";document.getElementById(\"createPost\").innerHTML = \'Close Post Form\';}else{document.getElementById(\"postForm\").style.display = \"none\";document.getElementById(\"createPost\").innerHTML = \'Create Post\';}}</script>"
    html += "<div style=display:none id=postForm>Title: <input type=text id=titleInput style=\"position:absolute;\"></input><br>Body: <textarea id=bodyInput></textarea><br>Username: <input type=text id=nameInput style=\"position:absolute;\"></input><br>"
    html += "<button style=background-color:BDFFBD type=button id=submitPost>Submit Post</button>"
    html += "<script type=text/javascript>document.getElementById(\"submitPost\").onclick = async function() {let postData = {\"title\":titleInput.value,\"content\":bodyInput.value,\"username\":nameInput.value};postData = JSON.stringify(postData); await fetch(\"https://tcze7o1n4k.execute-api.us-east-1.amazonaws.com/boards/" + boardData['id'] + "/posts\", {method:\"POST\", body:postData}); location.reload();}</script></div>"
    
    startTime = time.time()
    for postData in postArr:
        latestActivity = time.strftime('%m-%d-%Y at %H:%M:%S (UTC)', time.localtime(postData['latestActivity']))
        html += '<div style="border:3px; border-style:solid; width:80vw"><h4><a href="/boards/' + postData['parentId'] + '/posts/' + postData['id'] + '/comments">' + postData['title'] + "</a></h4>"
        html += "<button style=background-color:FFBDBD id=" + postData['id'] + ">Preview Post"
        html += "</button><script type=text/javascript>document.getElementById(\"" + postData['id'] + "\").onclick = function() {if(document.getElementById(\"" + postData['id'] + "\").innerHTML === \"Preview Post\") {document.getElementById(\"content" + postData['id'] + "\").style.display = \"block\"; document.getElementById(\"" + postData['id'] + "\").innerHTML = \"Hide Post\";} else {document.getElementById(\"content" + postData['id'] + "\").style.display = \"none\"; document.getElementById(\"" + postData['id'] + "\").innerHTML = \"Preview Post\";}}</script><div style=display:none id=\"content" + postData['id'] + "\">" + postData['content'] + "</div>"
        html += "<br>By " + postData['username'] + "<div style=\"text-align:right; position:relative; right:1%\">Latest comment: " + latestActivity + "</div></div>"

    cloudwatch.put_metric_data(
        MetricData = [
            {
                'MetricName': 'HTML Build Time',
                'Unit': 'Milliseconds',
                'Value': time.time() - startTime
            },
        ],
        Namespace='GetPost'
    )
    
    html += "</div></body></html>"
    
    cloudwatch.put_metric_data(
        MetricData = [
            {
                'MetricName': 'Query Time',
                'Unit': 'Milliseconds',
                'Value': time.time() - startTime
            },
        ],
        Namespace='GetPost'
    )

    return {
        'statusCode': 200,
        'headers': {
            'Content-Type': 'text/html',
            'Access-Control-Allow-Origin': '*'            
        },
        'body': html
    }
    