from google.cloud import pubsub_v1
import json

project_id = "data-eng-420421"
topic_id = "my-topic"

publisher = pubsub_v1.PublisherClient()
topic_path = publisher.topic_path(project_id, topic_id)

def pub_mssg(data):
    data = json.dumps(data).encode('utf-8')
    future = publisher.publish(topic_path, data)
    return future.result()

with open('bcsample.json', 'r') as file:
    data = json.load(file)

for date_key in data:
    records = data[date_key]
    for record in records:
        result = pub_mssg(record)
        print(f"Published message ID: {result}")

print(f"Published messages to {topic_path}.")
