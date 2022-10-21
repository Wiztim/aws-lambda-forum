AWS changed how API gateway works, how Python lambda functions return strings, and how information is sent to lambda. So this forum no longer works. 
The front page is displayed (and some quoation marks), but no other links work.

All the Python files in this Github are old and do not work.

See the front page in action at: https://wiztim.dev/
## Lambda Functions
* All functions written in python.
* The Get functions reads the database for the relevant boards/posts/comments and returns a HTML page that is used to display the forum.
* The GetById functions are used to help create the HTML in the Get functions.
* Create functions are used to create new posts/comments.
* CreateBoard was used to create the initial boards, and users shouldn't be able to access this.

## Building
* This is not intended to be ran locally.
* Set up requires configuring AWS DynamoDB, API Gateway, IAM Permissions, S3, and Lambda.

## Current Features
* Amazon DynamoDB is used to handle data storage.
* Amazon API Gateway is used to handle resource paths to the Lambda functions.
* Users may create a post and reply to a post with a comment


## Planned Features
* Considered features are a custom url, uploading images to posts/comments, quoting a post/comment, caching, sorting, user profiles, moderator roles, reporting, and post/comment deletion.
* Amazon S3 will be used to handle image hosting.
* Amazon Elasticache will be used to handle caching frequently accessed database items.
