from google.cloud import pubsub_v1
project_id = "data-eng-420421"
subscription_id = "my-sub"
subscriber = pubsub_v1.SubscriberClient()
subscription_path = subscriber.subscription_path(project_id, subscription_id)

def callback(message: pubsub_v1.subscriber.message.Message) -> None:
    print(f"Received message data: {message.data.decode('utf-8')}")
    message.ack()

streaming_pull_future = subscriber.subscribe(subscription_path, callback=callback)
print(f"Listening for messages on {subscription_path}..\n")

with subscriber:
        try:
                streaming_pull_future.result()
        except KeyboardInterrupt:
                streaming_pull_future.cancel() 
subscriber.close()
print("Subscription cleaned.")