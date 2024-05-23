import json
from google.cloud import pubsub_v1
from google.cloud import storage
from datetime import datetime
from threading import Timer

project_id = "data-eng-420421"
subscription_id = "archive-test-sub"
bucket_name = "inclass---8"
buffer_time = 60
print_status_interval = 300 
buffer = []
subscriber = pubsub_v1.SubscriberClient()
subscription_path = subscriber.subscription_path(project_id, subscription_id)
storage_client = storage.Client()

def upload_to_bucket(data, bucket_name):
    timestamp = datetime.utcnow().strftime('%Y%m%d%H%M%S')
    file_name = f"breadcrumb_{timestamp}.json"

    bucket = storage_client.get_bucket(bucket_name)

    blob = bucket.blob(file_name)
    blob.upload_from_string(json.dumps(data), content_type="application/json")

    print(f"Uploaded {file_name} to {bucket_name}")

def save_buffer():
    global buffer
    if buffer:
        upload_to_bucket(buffer, bucket_name)
        buffer = []

    Timer(buffer_time, save_buffer).start()

def print_status():
    print(f"Buffer contains {len(buffer)} messages.")
    Timer(print_status_interval, print_status).start()

def callback(message):
    global buffer
    buffer.append(json.loads(message.data.decode('utf-8')))
    message.ack()

save_buffer()

print_status()

streaming_pull_future = subscriber.subscribe(subscription_path, callback=callback)
print(f"Listening for messages on {subscription_path}...")

with subscriber:
    try:
        streaming_pull_future.result()
    except TimeoutError:
        streaming_pull_future.cancel()
