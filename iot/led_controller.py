# led_controller.py

def set_led_by_mood(mood):

    print("\n[LED UPDATE]")

    if mood == "HAPPY":

        print("GREEN LED ON")

    elif mood == "SLEEPY":

        print("BLUE LED ON")

    elif mood == "HUNGRY":

        print("RED LED ON")

    else:

        print("DEFAULT LED")
