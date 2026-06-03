from __future__ import annotations

import json
from typing import Any

import paho.mqtt.client as mqtt

from game_logic import state
from game_logic.event_handler import handle_event
from game_logic.logic import get_led_state


BROKER = "localhost"
PORT = 1883

TOPICS = {
    "LIGHT": "baekgyeong/sensor/light",
    "GYRO": "baekgyeong/sensor/gyro",
    "TILT": "baekgyeong/sensor/tilt",
    "BUTTON": "baekgyeong/input/button",
    "LCD_EVENT": "baekgyeong/event/lcd",
    "STATE_UPDATE": "baekgyeong/state/update",
    "LED_CONTROL": "baekgyeong/led/control",
    "ACTION_FEED": "baekgyeong/action/feed",
    "ACTION_PLAY": "baekgyeong/action/play",
    "ACTION_PET": "baekgyeong/action/pet",
    "ACTION_TEXT": "baekgyeong/action/text",
    "COMMAND": "baekgyeong/command",
}

SUBSCRIBE_TOPICS = [
    TOPICS["LIGHT"],
    TOPICS["GYRO"],
    TOPICS["TILT"],
    TOPICS["BUTTON"],
    TOPICS["LCD_EVENT"],
    TOPICS["ACTION_FEED"],
    TOPICS["ACTION_PLAY"],
    TOPICS["ACTION_PET"],
    TOPICS["ACTION_TEXT"],
    TOPICS["COMMAND"],
]


class BaekgyeongMqttClient:
    def __init__(
        self,
        broker: str = BROKER,
        port: int = PORT,
        client_id: str = "baekgyeong-server",
    ) -> None:
        self.broker = broker
        self.port = port
        self.client = mqtt.Client(client_id=client_id)
        self.client.on_connect = self._on_connect
        self.client.on_message = self._on_message

    def connect(self) -> None:
        self.client.connect(self.broker, self.port)

    def loop_forever(self) -> None:
        self.connect()
        self.client.loop_forever()

    def loop_start(self) -> None:
        self.connect()
        self.client.loop_start()

    def publish_json(self, topic: str, payload: dict[str, Any]) -> None:
        self.client.publish(topic, json.dumps(payload, ensure_ascii=False))

    def publish_state_update(self, result_event: dict[str, Any] | None = None) -> None:
        payload = {
            "source": "SYSTEM",
            "event": "STATE_UPDATED",
            "payload": state.get_state(),
        }
        if result_event is not None:
            payload["result_event"] = result_event
        self.publish_json(TOPICS["STATE_UPDATE"], payload)
        self.publish_json(
            TOPICS["LED_CONTROL"],
            {
                "source": "SYSTEM",
                "event": "LED_UPDATE",
                "payload": get_led_state(),
            },
        )

    def dispatch_event(self, event_message: dict[str, Any]) -> dict[str, Any]:
        normalized = normalize_event(event_message)
        result = handle_event(normalized)
        self.publish_state_update(result)
        return result

    def _on_connect(self, client, userdata, flags, reason_code, properties=None):
        print(f"[MQTT CONNECTED] {reason_code}")
        for topic in SUBSCRIBE_TOPICS:
            client.subscribe(topic)
            print(f"[MQTT SUBSCRIBE] {topic}")

    def _on_message(self, client, userdata, message):
        try:
            payload = json.loads(message.payload.decode("utf-8"))
        except json.JSONDecodeError:
            print("[MQTT MESSAGE ERROR] invalid json", message.topic, message.payload)
            return

        print(f"[MQTT RECEIVED] {message.topic}: {payload}")
        try:
            result = self.dispatch_event(payload)
            print("[GAME_LOGIC RESULT]", result)
        except Exception as exc:
            print("[GAME_LOGIC ERROR]", type(exc).__name__, exc)

    # Methods expected by ui/lcd/scenes/scene_manager.py
    def publish_feed_button_clicked(self) -> None:
        self.publish_lcd_event("FEED_BUTTON_CLICKED")

    def publish_feed_confirmed(self) -> None:
        self.publish_lcd_event("FEED_CONFIRMED")

    def publish_feed_cancelled(self) -> None:
        self.publish_lcd_event("FEED_CANCELLED")

    def publish_feed_finished(self, hunger_delta: int, caught_food_ids: list[int]) -> None:
        self.publish_lcd_event(
            "FEED_GAME_FINISHED",
            {
                "hunger_delta": hunger_delta,
                "caught_food_ids": caught_food_ids,
            },
        )

    def publish_sleep_button_clicked(self) -> None:
        self.publish_lcd_event("SLEEP_BUTTON_CLICKED")

    def publish_play_button_clicked(self) -> None:
        self.publish_lcd_event("PLAY_BUTTON_CLICKED")

    def publish_play_selected(self, game_type: str) -> None:
        self.publish_lcd_event("PLAY_GAME_SELECTED", {"game_type": game_type})

    def publish_play_finished(self, game_type: str, score: int, fun_delta: int) -> None:
        self.publish_lcd_event(
            "PLAY_GAME_FINISHED",
            {
                "game_type": game_type,
                "score": score,
                "fun_delta": fun_delta,
            },
        )

    def publish_text_button_clicked(self) -> None:
        self.publish_lcd_event("TEXT_BUTTON_CLICKED")

    def publish_stroke_attempt(self, date_string: str) -> None:
        self.publish_lcd_event("STROKE_ATTEMPT", {"date": date_string})

    def publish_new_baekgyeong(self) -> None:
        self.publish_lcd_event("NEW_BAEKGYEONG_REQUESTED")

    def publish_lcd_event(self, event: str, payload: dict[str, Any] | None = None) -> None:
        self.publish_json(
            TOPICS["LCD_EVENT"],
            {
                "source": "LCD",
                "event": event,
                "payload": payload or {},
            },
        )


def normalize_event(event_message: dict[str, Any]) -> dict[str, Any]:
    event = event_message.get("event")
    payload = event_message.get("payload") if isinstance(event_message.get("payload"), dict) else {}
    source = event_message.get("source", "MQTT")

    if event == "PET_DETECTED":
        return {"source": source, "event": "STROKE_ATTEMPT", "payload": payload}

    if event == "DEVICE_SHAKEN":
        shake_power = int(payload.get("shake_power", 0))
        return {
            "source": source,
            "event": "PLAY_GAME_FINISHED",
            "payload": {
                "game_type": "red_light_green_light",
                "score": shake_power * 10,
                "fun_delta": max(1, min(10, shake_power)),
            },
        }

    if event == "FOOD_CAUGHT":
        recovery = int(payload.get("recovery", payload.get("hunger_value", 0)))
        return {
            "source": source,
            "event": "FEED_GAME_FINISHED",
            "payload": {
                "caught_food_ids": [payload.get("food_id", payload.get("food_name", "unknown"))],
                "hunger_delta": recovery,
            },
        }

    return {"source": source, "event": event, "payload": payload}


if __name__ == "__main__":
    BaekgyeongMqttClient().loop_forever()
