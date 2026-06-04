# led_controller.py

WARNING_THRESHOLD = 10
RED_THRESHOLD = 30
YELLOW_THRESHOLD = 50


def get_led_color(value):

    if value <= WARNING_THRESHOLD:

        return "BLINK_RED"

    elif value <= RED_THRESHOLD:

        return "RED"

    elif value <= YELLOW_THRESHOLD:

        return "YELLOW"

    else:

        return "GREEN"


def get_led_status(state):

    return {

        "hunger":

            get_led_color(
                state["hunger"]
            ),

        "energy":

            get_led_color(
                state["energy"]
            ),

        "fun":

            get_led_color(
                state["fun"]
            )
    }


def update_status_leds(state):

    led_state = get_led_status(
        state
    )

    print("\n===== LED STATUS =====")

    print(
        "HUNGER:",
        led_state["hunger"]
    )

    print(
        "ENERGY:",
        led_state["energy"]
    )

    print(
        "FUN:",
        led_state["fun"]
    )


def warning_alert(stat_name):

    print("\n===== WARNING =====")

    print(
        f"{stat_name} CRITICAL"
    )

    print(
        "LED BLINKING"
    )


def show_evolution_effect():

    print("\n===== EVOLUTION =====")

    print(
        "LED RAINBOW EFFECT"
    )


def show_runaway_effect():

    print("\n===== RUNAWAY =====")

    print(
        "LED FLASH EFFECT"
    )
