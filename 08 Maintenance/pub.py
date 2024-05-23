from google.cloud import pubsub_v1
import json
import requests
import pandas as pd

# TODO(developer)
project_id = "data-eng-420421"
topic_id = "archive-test"

publisher = pubsub_v1.PublisherClient()
# The `topic_path` method creates a fully qualified identifier
# in the form `projects/{project_id}/topics/{topic_id}`
topic_path = publisher.topic_path(project_id, topic_id)



def publish_message(data):
    data = json.dumps(data).encode('utf-8')
    future = publisher.publish(topic_path, data)
    return future.result()

def get_vehicle_ids():
    doc_key = "10VKMye65LhbEgMLld5Ol3lOocWUwCaEgnPVgFQf9em0"
    url = f"https://docs.google.com/spreadsheets/d/{doc_key}/export?format=csv"
    response = requests.get(url)
    csv_data = response.content
    with open("vehicle_ids_sheet.csv", "wb") as file:
        file.write(csv_data)
    vehicle_ids = pd.read_csv("vehicle_ids_sheet.csv")['Doodle'].tolist()
    return vehicle_ids

def gather_and_publish_data():
    vehicle_ids = get_vehicle_ids()
    for vehicle_id in vehicle_ids:
        api_url = f"https://busdata.cs.pdx.edu/api/getBreadCrumbs?vehicle_id={vehicle_id}"
        response = requests.get(api_url)
        if response.status_code == 200:
            data = response.json()
            publish_message(json.dumps(data))
        else:
            print(f"Failed to fetch data for vehicle ID {vehicle_id}")


gather_and_publish_data()

print(f"Published messages to {topic_path}.")
