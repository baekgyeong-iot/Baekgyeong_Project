# led_controller.py

try:
    from gpio_config import (

        HUNGER_R_PIN,
        HUNGER_G_PIN,
        HUNGER_B_PIN,

        ENERGY_R_PIN,
        ENERGY_G_PIN,
        ENERGY_B_PIN,

        FUN_R_PIN,
        FUN_G_PIN,
        FUN_B_PIN
    )
except ImportError:
    from .gpio_config import (

        HUNGER_R_PIN,
        HUNGER_G_PIN,
        HUNGER_B_PIN,

        ENERGY_R_PIN,
        ENERGY_G_PIN,
        ENERGY_B_PIN,

        FUN_R_PIN,
        FUN_G_PIN,
        FUN_B_PIN
    )

WARNING_THRESHOLD = 10
RED_THRESHOLD = 30
YELLOW_THRESHOLD = 50


def get_led_color(value):

    if value >= YELLOW_THRESHOLD:
        return "GREEN"

    elif value >= RED_THRESHOLD:
        return "YELLOW"

    elif value >= WARNING_THRESHOLD:
        return "RED"

    else:
        return "BLINK_RED"
def get_rgb_output(color):

    if color == "OFF":

        return (0, 0, 0)

    if color == "WHITE":

        return (1, 1, 1)

    if color == "GREEN":

        return (0, 1, 0)

    elif color == "YELLOW":

        return (1, 1, 0)

    elif color == "RED":

        return (1, 0, 0)

    elif color == "BLINK_RED":

        return (1, 0, 0)

    return (0, 0, 0)




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
        f"HUNGER ({state['hunger']}) -> "
        f"{led_state['hunger']}"
    )

    print(
        f"ENERGY ({state['energy']}) -> "
        f"{led_state['energy']}"
    )

    print(
        f"FUN ({state['fun']}) -> "
        f"{led_state['fun']}"
    )

    if state["hunger"] <= WARNING_THRESHOLD:

        warning_alert(
            "HUNGER"
        )

    if state["energy"] <= WARNING_THRESHOLD:

        warning_alert(
            "ENERGY"
        )

    if state["fun"] <= WARNING_THRESHOLD:

        warning_alert(
            "FUN"
        )

    return led_state



def warning_alert(stat_name):

    print("\n===== WARNING =====")

    print(
        f"{stat_name} CRITICAL"
    )

    print(
        "[LED] BLINK_RED"
    )


def show_evolution_effect():

    print("\n===== EVOLUTION =====")

    print(
        "[LED] RAINBOW EFFECT"
    )


def show_runaway_effect():

    print("\n===== RUNAWAY =====")

    print(
        "[LED] FLASH EFFECT"
    )
