# mqtt_publisher.py

import json
import paho.mqtt.client as mqtt

BROKER = "localhost"
PORT = 1883

TOPICS = {
    "LIGHT": "baekgyeong/sensor/light",
    "GYRO": "baekgyeong/sensor/gyro",
    "TILT": "baekgyeong/sensor/tilt",
    "BUTTON": "baekgyeong/input/button",
    "LCD_EVENT": "baekgyeong/event/lcd",
    "STATE_UPDATE": "baekgyeong/state/update",
    "LED_CONTROL": "baekgyeong/led/control",
    "ACTION_FEED": "baekgyeong/action/feed",
    "ACTION_PLAY": "baekgyeong/action/play",
    "ACTION_PET": "baekgyeong/action/pet",
    "ACTION_TEXT": "baekgyeong/action/text",
    "COMMAND": "baekgyeong/command",
}

client = mqtt.Client()

mqtt_connected = False


def connect_mqtt():

    global mqtt_connected

    if mqtt_connected:
        return

   #try: #예외 처리 추가가 필요 할 시 수정할 것. 아래도 동일함
    client.connect(BROKER, PORT)
    client.loop_start()

    mqtt_connected = True

    print("[MQTT] Connected")

   #except Exception as e:    print(f"[MQTT] Connection Failed : {e}") 

    
  

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
