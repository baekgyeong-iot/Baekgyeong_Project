# sensor_reader.py

import random
import time

from mqtt_publisher import publish_event


def read_light_sensor():

    light_value = random.randint(0, 300)

    is_dark = light_value < 150

    event_data = {

        "source": "LIGHT_SENSOR",

        "event": "LIGHT_CHANGED",

        "payload": {

            "light_value": light_value,

            "is_dark": is_dark
        }
    }

    publish_event(
        "baekgyeong/sensor/light",
        event_data
    )


def read_feed_button():

    clicked = random.choice([True, False])

    if clicked:

        event_data = {

            "source": "LCD_BUTTON",

            "event": "FEED_BUTTON_CLICKED",

            "payload": {}
        }

        publish_event(
            "baekgyeong/button/feed",
            event_data
        )


def read_play_button():

    clicked = random.choice([True, False])

    if clicked:

        event_data = {

            "source": "TOUCH_SENSOR",

            "event": "PLAY_BUTTON_CLICKED",

            "payload": {}
        }

        publish_event(
            "baekgyeong/button/play",
            event_data
        )


if __name__ == "__main__":

    while True:

        read_light_sensor()

        read_feed_button()

        read_play_button()

        time.sleep(3)
