# speaker.py

import random


BABY_DIALOGS = [

    "안녕!",

    "배고파!",

    "놀아줘!",

    "졸려..."
]


CHILD_DIALOGS = [

    "오늘도 즐거워!",

    "같이 놀자!",

    "심심해!",

    "배가 고파!"
]


ADULT_DIALOGS = [

    "오늘 하루 어땠어?",

    "산책 가고 싶어.",

    "항상 고마워.",

    "행복해!"
]


HIGH_FAVOR_DIALOGS = [

    "정말 좋아해!",

    "항상 함께 있어줘서 고마워!",

    "선물을 준비했어!"
]


def play_sound(sound_name):

    print(
        f"[SPEAKER] PLAY_SOUND -> {sound_name}"
    )

    return sound_name


def play_warning_sound():

    return play_sound(
        "WARNING"
    )


def play_feed_sound():

    return play_sound(
        "FEED"
    )


def play_play_sound():

    return play_sound(
        "PLAY"
    )


def play_pet_sound():

    return play_sound(
        "PET"
    )


def play_evolution_sound():

    return play_sound(
        "EVOLUTION"
    )


def play_runaway_sound():

    return play_sound(
        "RUNAWAY"
    )

def speak_random_dialog(

    stage,

    favorability
):

    if favorability >= 80:

        dialog = random.choice(
            HIGH_FAVOR_DIALOGS
        )

    else:

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

    print(
         f"[DIALOG][{stage}][FAVOR={favorability}] {dialog}"
    )

    return dialog


def gift_event():

    gifts = [

        "꽃",

        "사탕",

        "편지",

        "장난감"
    ]

    gift = random.choice(
        gifts
    )

    print(
        f"[GIFT EVENT] {gift}"
    )

    return gift
