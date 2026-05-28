# mqtt_publisher.py

import json
import paho.mqtt.client as mqtt


BROKER = "localhost"

PORT = 1883


client = mqtt.Client()

client.connect(BROKER, PORT)


def publish_event(topic, event_data):

    payload = json.dumps(event_data)

    client.publish(topic, payload)

    print("\n[MQTT PUBLISH]")
    print("TOPIC :", topic)
    print("PAYLOAD :", payload)
