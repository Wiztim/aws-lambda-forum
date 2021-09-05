# aws-lambda-forum
These are the lambda functions for my serverless forum. All are written in python.

The Get functions reads the database for the relevant boards/posts/comments and returns a HTML page that is used to display the forum.
The GetById functions are used to help create the HTML in the Get functions.
Create functions are used to create new posts/comments.
CreateBoard was used to create the initial boards, and users shouldn't be able to access this.

Amazon DynamoDB is used to handle data storage.
Amazon API Gateway is used to handle resource paths to the Lambda functions.
Amazon S3 will be used to handle image hosting
Amazon Elasticache will be used to handle caching frequently accessed database items.

Current features are creating a post and replying to a post.
Considered features are a custom url, uploading images to posts/comments, quoting a post/comment, caching, sorting, user profiles, moderator roles, reporting, and post/comment deletion.
