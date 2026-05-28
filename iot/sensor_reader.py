# sensor_reader.py

import random
import time

from mqtt_publisher import (
    publish_event,
    TOPICS
)


def send_light_event():

    light_value = random.randint(0, 300)

    is_dark = light_value < 120


    event_data = {

        "source": "LIGHT_SENSOR",

        "event": "LIGHT_CHANGED",

        "payload": {

            "light_value": light_value,

            "is_dark": is_dark
        }
    }

    publish_event(
        TOPICS["LIGHT"],
        event_data
    )


def send_tilt_event():

    shake_power = random.randint(0, 10)

    event_data = {

        "source": "TILT_SENSOR",

        "event": "DEVICE_SHAKEN",

        "payload": {

            "shake_power": shake_power
        }
    }

    publish_event(
        TOPICS["TILT"],
        event_data
    )


def send_feed_event():

    food_list = [

        ("APPLE", 10),

        ("MEAT", 20),

        ("BREAD", 15),

        ("FISH", 25)
    ]

    food_name, recovery = random.choice(
        food_list
    )

    event_data = {

        "source": "TOUCH_SENSOR",

        "event": "FOOD_CAUGHT",

        "payload": {

            "food_name": food_name,

            "recovery": recovery
        }
    }

    publish_event(
        TOPICS["FEED"],
        event_data
    )


def send_pet_event():

    event_data = {

        "source": "LCD_TOUCH",

        "event": "PET_DETECTED",

        "payload": {}
    }

    publish_event(
        TOPICS["PET"],
        event_data
    )


def send_text_button_event():

    event_data = {

        "source": "TEXT_BUTTON",

        "event": "TEXT_BUTTON_CLICKED",

        "payload": {}
    }

    publish_event(
        TOPICS["TEXT"],
        event_data
    )


if __name__ == "__main__":

    for i in range(5):

        print(f"\n===== EVENT LOOP {i+1} =====")

        send_light_event()

        send_tilt_event()

        send_feed_event()

        send_pet_event()

        send_text_button_event()

        time.sleep(3)
