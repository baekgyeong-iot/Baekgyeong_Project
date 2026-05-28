# speaker.py

import random


BABY_DIALOGS = [

    "배고파...",

    "놀아줘!",

    "졸려...",

    "좋아해!"
]


CHILD_DIALOGS = [

    "오늘도 즐거워!",

    "같이 놀자!",

    "선물 줄까?",

    "배가 고파!"
]


ADULT_DIALOGS = [

    "오늘 하루 어땠어?",

    "산책 가고 싶어.",

    "항상 고마워.",

    "졸린데..."
]


GIFT_MESSAGES = [

    "작은 선물을 준비했어!",

    "이거 받아!",

    "널 위해 준비했어!"
]


def play_sound(sound_name):

    print("\n=========================")
    print(f"[SPEAKER SOUND] {sound_name}")
    print("=========================")


def play_warning_sound():

    play_sound("WARNING")


def play_feed_sound():

    play_sound("FEED")


def play_play_sound():

    play_sound("PLAY")


def play_sleep_sound():

    play_sound("SLEEP")


def play_pet_sound():

    play_sound("PET")


def speak_random_dialog(stage, favorability):

    if stage == "BABY":

        dialog = random.choice(
            BABY_DIALOGS
        )

    elif stage == "CHILD":

        dialog = random.choice(
            CHILD_DIALOGS
        )

    else:

        dialog = random.choice(
            ADULT_DIALOGS
        )

    print("\n=========================")
    print("[DIALOG]")
    print(dialog)
    print("=========================")


def gift_event():

    gift = random.choice(
        GIFT_MESSAGES
    )

    print("\n=========================")
    print("[GIFT EVENT]")
    print(gift)
    print("=========================")
