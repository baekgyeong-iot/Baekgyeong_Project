# mqtt_publisher.py

import json
import paho.mqtt.client as mqtt


BROKER = "localhost"
PORT = 1883


TOPICS = {

    "LIGHT": "baekgyeong/sensor/light",

    "TILT": "baekgyeong/sensor/tilt",

    "TOUCH": "baekgyeong/sensor/touch",

    "FEED": "baekgyeong/action/feed",

    "PLAY": "baekgyeong/action/play",

    "PET": "baekgyeong/action/pet",

    "TEXT": "baekgyeong/action/text"
}


client = mqtt.Client()

client.connect(BROKER, PORT)


def publish_event(topic, event_data):

    payload = json.dumps(event_data)

    client.publish(topic, payload)

    print("\n=========================")
    print("[MQTT PUBLISH]")
    print("TOPIC :", topic)
    print("PAYLOAD :", payload)
    print("=========================")
