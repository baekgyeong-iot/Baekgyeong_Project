# mqtt_publisher.py

import json
import paho.mqtt.client as mqtt

BROKER = "localhost"
PORT = 1883

TOPICS = {
    "LIGHT": "baekgyeong/sensor/light",
    "GYRO": "baekgyeong/sensor/gyro",
    "BUTTON": "baekgyeong/input/button",
    "LCD_EVENT": "baekgyeong/event/lcd",
    "ACTION_FEED": "baekgyeong/action/feed",
    "ACTION_PLAY": "baekgyeong/action/play",
    "ACTION_PET": "baekgyeong/action/pet",
    "ACTION_TEXT": "baekgyeong/action/text"
}

client = mqtt.Client()

mqtt_connected = False


def connect_mqtt():

    global mqtt_connected

    if mqtt_connected:
        return

    client.connect(BROKER, PORT)
    client.loop_start()

    mqtt_connected = True

    print("[MQTT] Connected")


def publish_event(topic, payload):

    connect_mqtt()

    client.publish(
        topic,
        json.dumps(
            payload,
            ensure_ascii=False
        )
    )

    print(
        f"[MQTT] Published -> {topic}"
    )
