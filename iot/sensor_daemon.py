from __future__ import annotations

import json
import time

import paho.mqtt.client as mqtt

try:
    import RPi.GPIO as GPIO  # type: ignore
except (ImportError, RuntimeError):
    GPIO = None

try:
    from gpio_config import GYRO_SENSOR_PIN, LIGHT_SENSOR_PIN
    from mqtt_publisher import BROKER, PORT, TOPICS
except ImportError:
    from .gpio_config import GYRO_SENSOR_PIN, LIGHT_SENSOR_PIN
    from .mqtt_publisher import BROKER, PORT, TOPICS


POLL_INTERVAL_SECONDS = 0.1
LIGHT_REPORT_INTERVAL_SECONDS = 0.5
SHAKE_COOLDOWN_SECONDS = 0.35
# 현재 조도 센서 모듈은 어두울 때 HIGH, 밝을 때 LOW로 들어온다.
# 반대로 동작하는 모듈이면 이 값을 True로 바꾸면 된다.
LIGHT_DARK_WHEN_LOW = False
SHAKE_ACTIVE_HIGH = True


class SensorDaemon:
    """조도/흔들림 센서 값을 MQTT 이벤트로 보내는 실행 루프."""

    def __init__(self, broker: str = BROKER, port: int = PORT) -> None:
        self.client = mqtt.Client(client_id="baekgyeong-sensor-daemon")
        self.broker = broker
        self.port = port
        self.last_is_dark = None
        self.last_light_sent_at = 0.0
        self.last_shake_at = 0.0
        self.last_gyro_value = 0

    def setup_gpio(self) -> None:
        if GPIO is None:
            print("[SENSOR] RPi.GPIO를 사용할 수 없어 센서 루프를 시작할 수 없습니다.")
            return

        GPIO.setmode(GPIO.BCM)
        GPIO.setup(LIGHT_SENSOR_PIN, GPIO.IN)
        GPIO.setup(GYRO_SENSOR_PIN, GPIO.IN)

    def connect(self) -> None:
        self.client.connect(self.broker, self.port)
        self.client.loop_start()
        print("[SENSOR] MQTT connected")

    def publish(self, topic: str, message: dict) -> None:
        self.client.publish(topic, json.dumps(message, ensure_ascii=False))

    def read_light(self) -> bool:
        value = GPIO.input(LIGHT_SENSOR_PIN)
        if LIGHT_DARK_WHEN_LOW:
            return value == GPIO.LOW
        return value == GPIO.HIGH

    def read_shake_active(self) -> bool:
        value = GPIO.input(GYRO_SENSOR_PIN)
        if SHAKE_ACTIVE_HIGH:
            return value == GPIO.HIGH
        return value == GPIO.LOW

    def publish_light_if_needed(self, is_dark: bool) -> None:
        now = time.time()
        changed = self.last_is_dark is None or is_dark != self.last_is_dark
        interval_elapsed = now - self.last_light_sent_at >= LIGHT_REPORT_INTERVAL_SECONDS

        if not changed and not interval_elapsed:
            return

        self.last_is_dark = is_dark
        self.last_light_sent_at = now
        self.publish(
            TOPICS["LIGHT"],
            {
                "source": "LIGHT_SENSOR",
                "event": "LIGHT_CHANGED",
                "payload": {
                    "is_dark": is_dark,
                },
            },
        )

    def publish_shake_if_needed(self, is_active: bool) -> None:
        now = time.time()
        previous_active = bool(self.last_gyro_value)
        self.last_gyro_value = int(is_active)

        if not is_active or previous_active or now - self.last_shake_at < SHAKE_COOLDOWN_SECONDS:
            return

        self.last_shake_at = now
        self.publish(
            TOPICS["GYRO"],
            {
                "source": "GYRO",
                "event": "DEVICE_SHAKEN",
                "payload": {
                    "shake_power": 1,
                },
            },
        )

    def run(self) -> None:
        self.setup_gpio()
        if GPIO is None:
            return

        self.connect()
        print("[SENSOR] Running. Ctrl+C로 종료")

        try:
            while True:
                self.publish_light_if_needed(self.read_light())
                self.publish_shake_if_needed(self.read_shake_active())
                time.sleep(POLL_INTERVAL_SECONDS)
        except KeyboardInterrupt:
            print("\n[SENSOR] Stopped")
        finally:
            self.client.loop_stop()
            GPIO.cleanup((LIGHT_SENSOR_PIN, GYRO_SENSOR_PIN))


if __name__ == "__main__":
    SensorDaemon().run()
