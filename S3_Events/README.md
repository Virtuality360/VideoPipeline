# Creating a Event Notification on Minio
## Web host
In the sidebar, go to notifications
Click on the 'Add Notification Target' button
Several different targets are available, we are interested in AMQP - for RabbitMQ

URL - Where our service is hosted, in the format amqp://username:password@url:port

Exchange (String) - Name of the exchange

Exchange Type (String) - Type of the Exchange (Direct, Topic, Fanout, Headers, Default, Dead Letter)

Routing Key (String) - Routing name

Mandatory (Bool) - Ignore undelivered messages when false

Durable (Bool) - When true, queue will survive a server restart

No Wait (Bool) - Non blocking message delivery when true

Internal (Bool) - Set to true for exchanges not to be used directly by publishers, but only when bound to other exchanges

Auto Deleted (Bool) - Auto delete queue when there are no consumers when true

Delivery Mode (Sring) - 1 for non-persistant, 2 for persistant queue

Queue Directory (Sring) - Staging directory for undelivered messages

Queue Limit (Sring) - Maximum limit for undelivered messages

Comment  (Sring) - A comment

---

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

---

A corresponding reciever is needed to be made in order to recieve messages.


