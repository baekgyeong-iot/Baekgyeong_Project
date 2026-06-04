# mqtt_publisher.py

import json
import paho.mqtt.client as mqtt


BROKER = "localhost"
PORT = 1883


TOPICS = {

    # 센서
    "LIGHT": "baekgyeong/sensor/light",
    "TILT": "baekgyeong/sensor/tilt",

    # 먹이 게임
    "FEED_START": "baekgyeong/game/feed/start",
    "FEED_CONTROL": "baekgyeong/game/feed/control",
    "FEED_RESULT": "baekgyeong/game/feed/result",

    # 놀이 게임
    "PLAY_START": "baekgyeong/game/play/start",
    "PLAY_RESULT": "baekgyeong/game/play/result",

    # 행동
    "PET": "baekgyeong/action/pet",
    "TEXT": "baekgyeong/action/text",

    # 이벤트
    "EVOLUTION": "baekgyeong/event/evolution",
    "RUNAWAY": "baekgyeong/event/runaway"
}


client = mqtt.Client()


def connect_mqtt():

    try:

        client.connect(BROKER, PORT)

        print("[MQTT] Connected")

    except Exception as e:

        print("[MQTT ERROR]")
        print(e)


def publish_event(topic, event_data):

    payload = json.dumps(
        event_data,
        ensure_ascii=False
    )

    client.publish(topic, payload)

    print("\n====================")
    print("[MQTT PUBLISH]")
    print("TOPIC :", topic)
    print("PAYLOAD :", payload)
    print("====================")


if __name__ == "__main__":

    connect_mqtt()
