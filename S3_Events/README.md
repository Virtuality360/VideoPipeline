# Creating a Event Notification on Minio
## Web host
In the sidebar, go to notifications
Click on the 'Add Notification Target' button
Several different targets are available, we are interested in AMQP - for RabbitMQ
URL - Where our service is hosted, in the format amqp://username:password@url:port
Exchange - 
Exchange Type -
Routing Key - 
Mandatory (Bool) - 
Drable (Bool) - 
No Wait (Bool) -
Internal  (Bool) -
Auto Deleted (Bool) -
Delivery Mode (Sring) -
Queue Directory (Sring) -
Queue Limit (Sring) -
Comment  (Sring) - A comment

Now that we have the notification set up, we need to set up the bucket to use that endpoint

Go to your buckets, and click on manage for the bucket that you want to set up
Click on 'Events'
Click 'Subscribe to Event'
The ARN dropdown has the list of all endpoints, we are looking for arn:minio:sqs::_:amqp
Prefix (String) - only trigger when a file with the correct prefix is called (everything before the '.' e.g. 
filename)
Suffix (String) - only trigger when a file with the matching suffix is called (everything after the '.' e.g. 
mp4) 
PUT - Whenever a file if uploaded
GET - Whenever a file is accessed
DELETE - Whenever a file is deleted

A corresponding reciever need to made to recieve messages.


