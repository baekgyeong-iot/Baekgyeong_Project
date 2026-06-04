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

    light_value = random.randint(0, 300)

    event_data = {

        "source": "LIGHT_SENSOR",

        "event": "LIGHT_CHANGED",

        "payload": {

            "light_value": light_value,

            "is_dark": light_value < 120
        }
    }

    publish_event(
        TOPICS["LIGHT"],
        event_data
    )


# =========================
# 흔들기 센서
# =========================

def send_shake_event():

    shake_power = random.randint(1, 10)

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


# =========================
# 먹이 게임 시작
# =========================

def start_feed_game():

    publish_event(

        TOPICS["FEED_START"],

        {
            "event": "FEED_GAME_STARTED"
        }
    )


# =========================
# 좌우 이동
# =========================

def move_left():

    publish_event(

        TOPICS["FEED_CONTROL"],

        {
            "event": "MOVE_LEFT"
        }
    )


def move_right():

    publish_event(

        TOPICS["FEED_CONTROL"],

        {
            "event": "MOVE_RIGHT"
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

        TOPICS["FEED_RESULT"],

        {

            "event": "FOOD_CAUGHT",

            "payload": {

                "food_name": food_name,

                "recovery": recovery
            }
        }
    )


# =========================
# 놀이 게임 시작
# =========================

def start_play_game():

    publish_event(

        TOPICS["PLAY_START"],

        {
            "event": "PLAY_GAME_STARTED"
        }
    )


# =========================
# LCD 터치
# =========================

def pet_detected():

    publish_event(

        TOPICS["PET"],

        {

            "event": "PET_DETECTED"
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

        TOPICS["TEXT"],

        {

            "event": "TEXT_BUTTON_CLICKED",

            "payload": {

                "stage": stage,

                "favorability": favorability
            }
        }
    )


# =========================
# 진화
# =========================

def evolution_event():

    publish_event(

        TOPICS["EVOLUTION"],

        {
            "event": "EVOLUTION"
        }
    )


# =========================
# 가출
# =========================

def runaway_event():

    publish_event(

        TOPICS["RUNAWAY"],

        {
            "event": "RUNAWAY"
        }
    )
