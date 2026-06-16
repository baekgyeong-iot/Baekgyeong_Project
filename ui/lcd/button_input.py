from __future__ import annotations

from dataclasses import dataclass

import pygame

try:
    import RPi.GPIO as GPIO  # type: ignore
except (ImportError, RuntimeError):
    GPIO = None

try:
    from iot.gpio_config import LEFT_BUTTON_PIN, RIGHT_BUTTON_PIN
except ImportError:
    LEFT_BUTTON_PIN = 12
    RIGHT_BUTTON_PIN = 17


LONG_PRESS_MS = 800


@dataclass
class ButtonState:
    is_down: bool = False
    down_at: int = 0
    long_sent: bool = False


class ButtonInput:
    """왼쪽/오른쪽 물리 버튼을 짧게 누름/길게 누름 이벤트로 변환한다."""

    def __init__(self, long_press_ms: int = LONG_PRESS_MS):
        self.long_press_ms = long_press_ms
        self.states = {
            "LEFT": ButtonState(),
            "RIGHT": ButtonState(),
        }
        self.gpio_ready = GPIO is not None

        if self.gpio_ready:
            GPIO.setmode(GPIO.BCM)
            for pin in (LEFT_BUTTON_PIN, RIGHT_BUTTON_PIN):
                GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

    def close(self) -> None:
        if self.gpio_ready:
            GPIO.cleanup((LEFT_BUTTON_PIN, RIGHT_BUTTON_PIN))

    def poll(self) -> list[tuple[str, str]]:
        if not self.gpio_ready:
            return []

        now = pygame.time.get_ticks()
        actions = []
        pin_by_direction = {
            "LEFT": LEFT_BUTTON_PIN,
            "RIGHT": RIGHT_BUTTON_PIN,
        }

        for direction, pin in pin_by_direction.items():
            pressed = GPIO.input(pin) == GPIO.LOW
            state = self.states[direction]

            if pressed and not state.is_down:
                state.is_down = True
                state.down_at = now
                state.long_sent = False

            elif pressed and state.is_down and not state.long_sent:
                if now - state.down_at >= self.long_press_ms:
                    actions.append(("LONG", direction))
                    state.long_sent = True

            elif not pressed and state.is_down:
                if not state.long_sent:
                    actions.append(("SHORT", direction))
                state.is_down = False
                state.down_at = 0
                state.long_sent = False

        return actions
