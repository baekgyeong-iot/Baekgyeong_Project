from __future__ import annotations

import json
import time
from typing import Any

import paho.mqtt.client as mqtt

try:
    import RPi.GPIO as GPIO  # type: ignore
except (ImportError, RuntimeError):
    GPIO = None

try:
    from gpio_config import (
        ENERGY_B_PIN,
        ENERGY_G_PIN,
        ENERGY_R_PIN,
        FUN_B_PIN,
        FUN_G_PIN,
        FUN_R_PIN,
        HUNGER_B_PIN,
        HUNGER_G_PIN,
        HUNGER_R_PIN,
    )
    from led_controller import get_rgb_output
    from mqtt_publisher import BROKER, PORT, TOPICS
except ImportError:
    from .gpio_config import (
        ENERGY_B_PIN,
        ENERGY_G_PIN,
        ENERGY_R_PIN,
        FUN_B_PIN,
        FUN_G_PIN,
        FUN_R_PIN,
        HUNGER_B_PIN,
        HUNGER_G_PIN,
        HUNGER_R_PIN,
    )
    from .led_controller import get_rgb_output
    from .mqtt_publisher import BROKER, PORT, TOPICS


# 사진 속 R/G/B/- 형태 RGB 모듈은 보통 공통 캐소드라 HIGH가 켜짐이다.
# 불이 반대로 동작하면 False로 바꾸면 된다.
LED_ACTIVE_HIGH = True
LED_BRIGHTNESS = 0.25
BLINK_INTERVAL_SECONDS = 0.35

LED_PINS = {
    "hunger": (HUNGER_R_PIN, HUNGER_G_PIN, HUNGER_B_PIN),
    "energy": (ENERGY_R_PIN, ENERGY_G_PIN, ENERGY_B_PIN),
    "fun": (FUN_R_PIN, FUN_G_PIN, FUN_B_PIN),
}


def pwm_duty(on: int) -> float:
    duty = 100.0 * LED_BRIGHTNESS if on else 0.0
    if LED_ACTIVE_HIGH:
        return duty
    return 100.0 - duty


class LedDaemon:
    """백엔드가 발행한 LED_CONTROL MQTT 메시지를 실제 RGB LED로 출력한다."""

    def __init__(self, broker: str = BROKER, port: int = PORT) -> None:
        self.client = mqtt.Client(client_id="baekgyeong-led-daemon")
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message
        self.broker = broker
        self.port = port
        self.current_payload: dict[str, Any] = {}
        self.blink_on = True
        self.last_blink_at = 0.0
        self.pwms = {}

    def setup_gpio(self) -> None:
        if GPIO is None:
            print("[LED] RPi.GPIO를 사용할 수 없어 LED 루프를 시작할 수 없습니다.")
            return

        GPIO.setmode(GPIO.BCM)
        for pins in LED_PINS.values():
            for pin in pins:
                GPIO.setup(pin, GPIO.OUT)
                pwm = GPIO.PWM(pin, 1000)
                pwm.start(pwm_duty(0))
                self.pwms[pin] = pwm
        self.turn_all_off()

    def turn_all_off(self) -> None:
        for name in LED_PINS:
            self.set_rgb(name, "OFF")

    def on_connect(self, client, userdata, flags, reason_code, properties=None):
        print(f"[LED] MQTT connected: {reason_code}")
        client.subscribe(TOPICS["LED_CONTROL"])
        print(f"[LED] subscribe {TOPICS['LED_CONTROL']}")

    def on_message(self, client, userdata, message) -> None:
        try:
            data = json.loads(message.payload.decode("utf-8"))
        except json.JSONDecodeError:
            print("[LED] invalid json", message.payload)
            return

        payload = data.get("payload", {})
        if isinstance(payload, dict):
            if (
                getattr(message, "retain", False)
                and payload.get("game_led") in {"LEFT", "RIGHT"}
            ):
                self.turn_all_off()
                return
            self.current_payload = payload
            self.apply_payload()

    def set_rgb(self, name: str, color: str) -> None:
        if GPIO is None:
            return

        r_pin, g_pin, b_pin = LED_PINS[name]
        r, g, b = get_rgb_output(color)
        self.pwms[r_pin].ChangeDutyCycle(pwm_duty(r))
        self.pwms[g_pin].ChangeDutyCycle(pwm_duty(g))
        self.pwms[b_pin].ChangeDutyCycle(pwm_duty(b))

    def apply_payload(self) -> None:
        game_led = self.current_payload.get("game_led", "OFF")

        if game_led == "LEFT":
            self.set_rgb("hunger", "WHITE")
            self.set_rgb("energy", "OFF")
            self.set_rgb("fun", "OFF")
            return

        if game_led == "RIGHT":
            self.set_rgb("hunger", "OFF")
            self.set_rgb("energy", "WHITE")
            self.set_rgb("fun", "OFF")
            return

        for name, key in {
            "hunger": "hunger_led",
            "energy": "energy_led",
            "fun": "fun_led",
        }.items():
            color = self.current_payload.get(key, "OFF")
            if color == "BLINK_RED":
                self.set_rgb(name, "RED" if self.blink_on else "OFF")
            else:
                self.set_rgb(name, color)

    def update_blink(self) -> None:
        if not any(value == "BLINK_RED" for value in self.current_payload.values()):
            return

        now = time.time()
        if now - self.last_blink_at < BLINK_INTERVAL_SECONDS:
            return

        self.last_blink_at = now
        self.blink_on = not self.blink_on
        self.apply_payload()

    def run(self) -> None:
        self.setup_gpio()
        if GPIO is None:
            return

        self.client.connect(self.broker, self.port)
        self.client.loop_start()
        print("[LED] Running. Ctrl+C로 종료")

        try:
            while True:
                self.update_blink()
                time.sleep(0.05)
        except KeyboardInterrupt:
            print("\n[LED] Stopped")
        finally:
            self.client.loop_stop()
            self.turn_all_off()
            for pwm in self.pwms.values():
                pwm.stop()
            GPIO.cleanup()


if __name__ == "__main__":
    LedDaemon().run()
