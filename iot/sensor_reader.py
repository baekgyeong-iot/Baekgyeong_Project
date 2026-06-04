# sensor_reader.py

import random

from mqtt_publisher import (
    publish_event,
    TOPICS
)


# =========================
# 조도 센서
# =========================

def send_light_event():

    light_value = random.randint(0,300)

    is_dark = light_value < 100

    publish_event(

        TOPICS["LIGHT"],

        {
            "source": "LIGHT_SENSOR",

            "event": "LIGHT_CHANGED",

            "payload": {
                "light_value": light_value,
                "is_dark": is_dark
            }
        }
    )

# =========================
# 흔들기 센서
# =========================

def send_shake_event():

    shake_power = random.randint(1, 10)

    publish_event(

        TOPICS["GYRO"],

        {
            "source": "GYRO",

            "event": "DEVICE_SHAKEN",

            "payload": {
                "shake_power": shake_power
            }
        }
    )
 
# =========================
# 먹이 먹음
# =========================

def food_caught():

    foods = [

        ("APPLE", 10),

        ("BREAD", 15),

        ("MEAT", 20),

        ("FISH", 25)
    ]

    food_name, recovery = random.choice(
        foods
    )

    publish_event(

        TOPICS["ACTION_FEED"],

        {
            "source": "BUTTON",
            
            "event": "FOOD_CAUGHT",

            "payload": {

                "food_name": food_name,

                "recovery": recovery
            }
        }
    )



# =========================
# LCD 터치
# =========================

def pet_detected():

    publish_event(

        TOPICS["ACTION_PET"],

        {
            "source": "TOUCH",
            
            "event": "PET_DETECTED",

            "payload": {}
        }
    )


# =========================
# 대화 버튼
# =========================

def text_button_clicked(
    stage="BABY",
    favorability=0
):

    publish_event(

        TOPICS["ACTION_TEXT"],

        {
            "source": "BUTTON",
            
            "event": "TEXT_BUTTON_CLICKED",

            "payload": {

                "stage": stage,

                "favorability": favorability
            }
        }
    )


