"""Publishes multiple messages to a Pub/Sub topic with an error handler."""
import time
import random
import json
from time import sleep

from google.cloud import pubsub_v1

project_id = "ilan-uzan"
topic_id = "test"

publisher = pubsub_v1.PublisherClient()
topic_path = publisher.topic_path(project_id, topic_id)

possible_entity_types = ["chair", "table", "clicker", "couch", "bed"]

for i in range(10000000):
    data = json.dumps({"id": i, "type": possible_entity_types[random.randint(0, 4)], "duration": random.random() * 115})

    # When you publish a message, the client returns a future.
    future = publisher.publish(topic_path, data.encode("utf-8"))
    print(future.result())

    sleep(0.1)

print(f"Published messages with error handler to {topic_path}.")