from __future__ import annotations

import json
import sys
from pathlib import Path
from urllib.error import URLError
from urllib.request import Request, urlopen
from scenes.runaway_scene import RunawayScene
from scenes.sleep_scene import SleepScene

import pygame
import time

CURRENT_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = CURRENT_DIR.parents[1]

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from asset_loader import load_fonts, load_food_sprites, load_icons, load_sprites
from button_input import ButtonInput
from game_logic import event_handler, state as local_state
from scenes.scene_manager import SceneManager

SCREEN_WIDTH = 480
SCREEN_HEIGHT = 320
FPS = 30
TICK_MS = 5000
API_BASE_URL = "http://localhost:5050/api"


class LogicBridge:
    def __init__(self, lcd_state: dict) -> None:
        self.lcd_state = lcd_state
        self.message_lock_until = 0
        self.last_log_key = None

    def _get_backend_state(self) -> dict | None:
        try:
            with urlopen(f"{API_BASE_URL}/state", timeout=0.2) as response:
                return json.loads(response.read().decode("utf-8"))
        except (OSError, URLError, TimeoutError, json.JSONDecodeError):
            return None

    def _get_backend_logs(self) -> list[dict]:
        try:
            with urlopen(f"{API_BASE_URL}/logs?limit=8", timeout=0.2) as response:
                data = json.loads(response.read().decode("utf-8"))
                logs = data.get("logs", [])
                return logs if isinstance(logs, list) else []
        except (OSError, URLError, TimeoutError, json.JSONDecodeError):
            return []

    def _log_key(self, log: dict) -> str:
        payload = log.get("payload", {})
        try:
            payload_text = json.dumps(payload, sort_keys=True, ensure_ascii=False)
        except TypeError:
            payload_text = str(payload)
        return f"{log.get('timestamp')}|{log.get('event')}|{payload_text}"

    def poll_backend_events(self) -> list[dict]:
        logs = self._get_backend_logs()
        if not logs:
            return []

        if self.last_log_key is None:
            self.last_log_key = self._log_key(logs[-1])
            return []

        new_logs = []
        for log in reversed(logs):
            if self._log_key(log) == self.last_log_key:
                break
            new_logs.append(log)

        self.last_log_key = self._log_key(logs[-1])
        return list(reversed(new_logs))

    def sync_state(self) -> bool:
        current = self._get_backend_state()
        connected = current is not None
        if current is None:
            current = local_state.get_state()

        self.lcd_state.update(current)
        if time.time() > self.message_lock_until:
            self.lcd_state["current_message"] = make_message(current)
        return connected

    def dispatch(self, event: str, payload: dict | None = None) -> dict:
        message = {
            "source": "LCD",
            "event": event,
            "payload": payload or {},
        }

        try:
            request = Request(
                f"{API_BASE_URL}/event",
                data=json.dumps(message).encode("utf-8"),
                headers={"Content-Type": "application/json"},
                method="POST",
            )
            with urlopen(request, timeout=0.3) as response:
                data = json.loads(response.read().decode("utf-8"))
                current = data.get("state", {})
        except (OSError, URLError, TimeoutError, json.JSONDecodeError):
            event_handler.handle_event(message)
            current = local_state.get_state()

        self.lcd_state.update(current)
        self.lcd_state["current_message"] = make_message(current)
        return current

    def publish_feed_button_clicked(self) -> None:
        self.dispatch("FEED_BUTTON_CLICKED")

    def publish_feed_confirmed(self) -> None:
        self.dispatch("FEED_CONFIRMED")

    def publish_feed_cancelled(self) -> None:
        self.dispatch("FEED_CANCELLED")

    def publish_feed_finished(self, hunger_delta: int, caught_food_ids: list[int]) -> None:
        self.dispatch(
            "FEED_GAME_FINISHED",
            {
                "hunger_delta": hunger_delta,
                "caught_food_ids": caught_food_ids,
            },
        )

    def publish_sleep_button_clicked(self) -> None:
        self.dispatch("SLEEP_BUTTON_CLICKED")

    def publish_play_button_clicked(self) -> None:
        self.dispatch("PLAY_BUTTON_CLICKED")

    def publish_play_selected(self, game_type: str) -> None:
        self.dispatch("PLAY_GAME_SELECTED", {"game_type": game_type})

    def publish_play_finished(self, game_type: str, score: int, fun_delta: int) -> None:
        self.dispatch(
            "PLAY_GAME_FINISHED",
            {
                "game_type": game_type,
                "score": score,
                "fun_delta": fun_delta,
            },
        )

    def publish_text_button_clicked(self) -> None:
        self.dispatch("TEXT_BUTTON_CLICKED")

    def publish_stroke_attempt(self, date_string: str) -> None:
        self.dispatch("STROKE_ATTEMPT", {"date": date_string})

    def publish_new_baekgyeong(self) -> None:
        self.dispatch("NEW_BAEKGYEONG_REQUESTED")

    def publish_led_left(self) -> None:
        self.dispatch("LED_LEFT")

    def publish_led_right(self) -> None:
        self.dispatch("LED_RIGHT")

    def publish_led_off(self) -> None:
        self.dispatch("LED_OFF")

def make_message(current: dict) -> str:
    if current.get("is_runaway"):
        return "백경이가 가출했습니다."
    if current.get("is_sleeping"):
        return "쿨쿨... 백경이가 자고 있어요."
    if current.get("hunger", 0) <= 20:
        return "배고파요... 크릴새우 주세요!"
    if current.get("energy", 0) <= 20:
        return "졸려요... 불을 꺼주세요."
    if current.get("fun", 0) <= 20:
        return "심심해요. 같이 놀아요!"
    return "백경이와 즐거운 시간을 보내세요."

def main() -> int:
    pygame.init()
    pygame.display.set_caption("Baekgyeong LCD")
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    clock = pygame.time.Clock()

    font_sm, font_md, font_lg = load_fonts()
    icons = load_icons()
    sprites = load_sprites()
    food_sprites = load_food_sprites()

    lcd_state: dict = {}
    bridge = LogicBridge(lcd_state)
    backend_connected = bridge.sync_state()

    scene_manager = SceneManager(
        screen,
        lcd_state,
        sprites,
        icons,
        food_sprites,
        font_sm,
        font_md,
        font_lg,
    )

    scene_manager.mqtt_client = bridge

    if lcd_state.get("is_runaway"):
        scene_manager.change_scene(
            "RUNAWAY_EVENT_TRIGGERED",
            {
                "is_runaway": True
            }
        )

    elif lcd_state.get("is_sleeping"):
        scene_manager.change_scene("SLEEP_STARTED")

    last_tick = pygame.time.get_ticks()
    last_sync = 0
    button_input = ButtonInput()
    keyboard_buttons = {
        pygame.K_LEFT: {
            "direction": "LEFT",
            "is_down": False,
            "down_at": 0,
            "long_sent": False,
        },
        pygame.K_RIGHT: {
            "direction": "RIGHT",
            "is_down": False,
            "down_at": 0,
            "long_sent": False,
        },
    }
    running = True

    try:
        while running:
            now = pygame.time.get_ticks()

            if now - last_sync >= 500:
                backend_connected = bridge.sync_state()
                for log in bridge.poll_backend_events():
                    event_name = log.get("event")
                    payload = log.get("payload", {})
                    if event_name in {
                        "GIFT_EVENT_TRIGGERED",
                        "EVO_EVENT_TRIGGERED",
                        "RUNAWAY_EVENT_TRIGGERED",
                        "GYRO_CHANGED",
                        "DEVICE_SHAKEN",
                    }:
                        scene_manager.handle_system_event(event_name, payload)
                    elif (
                        event_name == "PLAY_GAME_FINISHED"
                        and
                        payload.get("game_type") == "red_light_green_light"
                        and
                        scene_manager.current_scene.__class__.__name__ == "GyroGameScene"
                    ):
                        scene_manager.handle_system_event(
                            event_name,
                            {
                                **payload,
                                "already_recorded": True,
                            },
                        )
                last_sync = now
        
            if (
                lcd_state.get("is_sleeping")
                and
                not isinstance(
                    scene_manager.current_scene,
                    SleepScene
                )
            ):
                scene_manager.change_scene("SLEEP_STARTED")

            elif (
                not lcd_state.get("is_sleeping")
                and
                isinstance(
                    scene_manager.current_scene,
                    SleepScene
                )
            ):
                scene_manager.change_scene(
                    "SLEEP_ENDED",
                    {
                        "current_energy":
                        lcd_state.get(
                            "energy",
                            0
                        )
                    }
                )

            if (
                lcd_state.get("is_runaway")
                and
                not isinstance(
                    scene_manager.current_scene,
                    RunawayScene
                )
            ):
                scene_manager.change_scene(
                    "RUNAWAY_EVENT_TRIGGERED"
                )
        
            elif (
                not lcd_state.get("is_runaway")
                and
                isinstance(
                    scene_manager.current_scene,
                    RunawayScene
                )
            ):
                scene_manager.go_home()

            if not backend_connected and now - last_tick >= TICK_MS:
                bridge.dispatch("TIME_TICK")
                last_tick += TICK_MS

            for action, direction in button_input.poll():
                if action == "SHORT":
                    scene_manager.handle_button_short(direction)
                elif action == "LONG":
                    scene_manager.handle_button_long(direction)

            for key_state in keyboard_buttons.values():
                if (
                    key_state["is_down"]
                    and
                    not key_state["long_sent"]
                    and
                    now - key_state["down_at"] >= button_input.long_press_ms
                ):
                    scene_manager.handle_button_long(key_state["direction"])
                    key_state["long_sent"] = True

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

                elif event.type == pygame.KEYDOWN:
                    if event.key in (pygame.K_ESCAPE, pygame.K_q):
                        running = False
                    elif event.key == pygame.K_t:
                        bridge.dispatch("TIME_TICK")
                        last_tick = now
                    elif event.key == pygame.K_r:
                        bridge.dispatch("NEW_BAEKGYEONG_REQUESTED")
                        scene_manager.go_home()
                        last_tick = now
                    elif event.key in keyboard_buttons:
                        key_state = keyboard_buttons[event.key]
                        if not key_state["is_down"]:
                            key_state["is_down"] = True
                            key_state["down_at"] = now
                            key_state["long_sent"] = False
                    elif event.key in (pygame.K_RETURN, pygame.K_SPACE):
                        scene_manager.handle_button_long("RIGHT")
                    else:
                        scene_manager.handle_key(event.key)

                elif event.type == pygame.KEYUP and event.key in keyboard_buttons:
                    key_state = keyboard_buttons[event.key]
                    if key_state["is_down"] and not key_state["long_sent"]:
                        scene_manager.handle_button_short(key_state["direction"])
                    key_state["is_down"] = False
                    key_state["down_at"] = 0
                    key_state["long_sent"] = False

                elif (
                    scene_manager.current_scene
                    and
                    hasattr(
                        scene_manager.current_scene,
                        "handle_event"
                    )
                ):
                    scene_manager.current_scene.handle_event(
                        event
                    )

            scene_manager.draw()
            pygame.display.flip()
            clock.tick(FPS)
    finally:
        button_input.close()
        pygame.quit()
    return 0

if __name__ == "__main__":
    sys.exit(main())
