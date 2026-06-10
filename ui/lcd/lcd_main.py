from __future__ import annotations

import json
import sys
from pathlib import Path
from urllib.error import URLError
from urllib.request import Request, urlopen

import pygame
import time

CURRENT_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = CURRENT_DIR.parents[1]

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from asset_loader import load_fonts, load_food_sprites, load_icons, load_sprites
from game_logic import event_handler, state as local_state
from scenes.scene_manager import SceneManager

SCREEN_WIDTH = 480
SCREEN_HEIGHT = 320
FPS = 30
TICK_MS = 60000
API_BASE_URL = "http://localhost:5050/api"


class LogicBridge:
    def __init__(self, lcd_state: dict) -> None:
        self.lcd_state = lcd_state
        self.message_lock_until = 0

    def _get_backend_state(self) -> dict | None:
        try:
            with urlopen(f"{API_BASE_URL}/state", timeout=0.2) as response:
                return json.loads(response.read().decode("utf-8"))
        except (OSError, URLError, TimeoutError, json.JSONDecodeError):
            return None

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

    last_tick = pygame.time.get_ticks()
    last_sync = 0
    running = True

    while running:
        now = pygame.time.get_ticks()

        if now - last_sync >= 500:
            backend_connected = bridge.sync_state()
            last_sync = now

        if not backend_connected and now - last_tick >= TICK_MS:
            bridge.dispatch("TIME_TICK")
            last_tick = now

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
                else:
                    scene_manager.handle_key(event.key)

            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                scene_manager.handle_click(*event.pos)

        scene_manager.draw()
        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()
    return 0

if __name__ == "__main__":
    sys.exit(main())
