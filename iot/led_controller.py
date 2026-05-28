# led_controller.py

WARNING_THRESHOLD = 10

YELLOW_THRESHOLD = 50
RED_THRESHOLD = 30


def get_led_color(value):

    if value <= WARNING_THRESHOLD:

        return "BLINK_RED"

    elif value <= RED_THRESHOLD:

        return "RED"

    elif value <= YELLOW_THRESHOLD:

        return "YELLOW"

    else:

        return "GREEN"


def update_status_leds(state):

    hunger_color = get_led_color(
        state["hunger"]
    )

    energy_color = get_led_color(
        state["energy"]
    )

    fun_color = get_led_color(
        state["fun"]
    )

    print("\n=========================")
    print("[LED STATUS UPDATE]")

    print(f"HUNGER LED : {hunger_color}")
    print(f"ENERGY LED : {energy_color}")
    print(f"FUN LED : {fun_color}")

    print("=========================")


def warning_alert(stat_name):

    print("\n=========================")
    print("[WARNING ALERT]")
    print(f"{stat_name} VALUE CRITICAL")
    print("LED BLINKING")
    print("=========================")
