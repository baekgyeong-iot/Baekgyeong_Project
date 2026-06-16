import pygame
import random

SCREEN_WIDTH = 480
SCREEN_HEIGHT = 320

COLOR_BG = (73, 116, 181)
COLOR_WHITE = (255, 255, 255)
COLOR_DARK = (32, 55, 88)

MAX_ROUND = 5
FLASH_INTERVAL_MS = 800


class MemoryGameScene:
    def __init__(
        self,
        screen,
        state,
        sprites,
        mqtt_client,
        font_sm,
        font_md,
        font_lg
    ):
        self.screen = screen
        self.state = state
        self.sprites = sprites
        self.mqtt_client = mqtt_client

        self.font_sm = font_sm
        self.font_md = font_md
        self.font_lg = font_lg

        self.finished = False
        self.score = 0
        self.round = 1

        self.active_button = None
        self.button_press_time = 0

        self.sequence = []
        self.user_inputs = []
        self.showing_sequence = True
        self.sequence_index = 0
        self.last_flash = pygame.time.get_ticks()
        self.led_off_sent = False
        self.published_sequence_index = None

        self.generate_round()

    def handle_click(self, mx, my):
        return None

    def generate_round(self):
        self.sequence = [
            random.choice(["LEFT", "RIGHT"])
            for _ in range(self.round + 2)
        ]
        self.user_inputs = []
        self.sequence_index = 0
        self.showing_sequence = True
        self.last_flash = pygame.time.get_ticks()
        self.led_off_sent = False
        self.published_sequence_index = None
        self.publish_current_led()

    def draw(self):
        self.screen.fill(COLOR_BG)
        self.draw_header()
        self.draw_led_instruction()
        self.draw_character()
        self.draw_info()

    def draw_header(self):
        title = self.font_md.render(
            f"암기게임 ROUND {self.round}",
            True,
            COLOR_WHITE
        )
        self.screen.blit(title, (20, 20))

        score = self.font_md.render(
            f"점수 {self.score}",
            True,
            COLOR_WHITE
        )
        self.screen.blit(score, (340, 20))

    def draw_led_instruction(self):
        if self.showing_sequence:
            label = "LED 순서를 기억하세요"
        else:
            label = "실제 왼쪽/오른쪽 버튼을 입력하세요"

        panel = pygame.Rect(70, 80, 340, 44)
        pygame.draw.rect(
            self.screen,
            COLOR_DARK,
            panel,
            border_radius=12
        )

        text = self.font_md.render(label, True, COLOR_WHITE)
        self.screen.blit(text, text.get_rect(center=panel.center))

    def draw_character(self):
        stage = self.state.get("growth_stage", "BABY")
        basic = self.sprites.get(stage, {}).get("BASIC", [])

        if not basic:
            return

        frame = (pygame.time.get_ticks() // 500) % len(basic)
        sprite = basic[frame]
        self.screen.blit(sprite, sprite.get_rect(center=(240, 180)))

    def draw_info(self):
        msg = "순서를 기억하세요" if self.showing_sequence else "버튼을 입력하세요"
        text = self.font_sm.render(msg, True, COLOR_WHITE)
        self.screen.blit(
            text,
            (
                SCREEN_WIDTH // 2 - text.get_width() // 2,
                280
            )
        )

    def update(self):
        if not self.showing_sequence:
            return

        now = pygame.time.get_ticks()

        if now - self.last_flash < FLASH_INTERVAL_MS // 2:
            self.publish_current_led()
        else:
            self.publish_led_off_once()

        if now - self.last_flash > FLASH_INTERVAL_MS:
            self.sequence_index += 1
            self.last_flash = now
            self.led_off_sent = False

            if self.sequence_index >= len(self.sequence):
                self.showing_sequence = False
                self.publish_led_off_once()
            else:
                self.publish_current_led()

    def publish_current_led(self):
        if (
            not self.mqtt_client
            or not self.showing_sequence
            or self.sequence_index >= len(self.sequence)
            or self.published_sequence_index == self.sequence_index
        ):
            return

        direction = self.sequence[self.sequence_index]

        if direction == "LEFT":
            self.mqtt_client.publish_led_left()
        else:
            self.mqtt_client.publish_led_right()

        self.published_sequence_index = self.sequence_index
        self.led_off_sent = False

    def publish_led_off_once(self):
        if self.mqtt_client and not self.led_off_sent:
            self.mqtt_client.publish_led_off()
            self.led_off_sent = True

    def handle_short_press(self, direction):
        self.handle_button(direction)
        return None

    def handle_button(self, direction):
        if self.showing_sequence:
            return

        self.active_button = direction
        self.button_press_time = pygame.time.get_ticks()
        self.user_inputs.append(direction)

        idx = len(self.user_inputs) - 1
        if self.sequence[idx] != direction:
            self.finished = True
            if self.mqtt_client:
                self.mqtt_client.publish_led_off()
            return

        self.score += 50

        if len(self.user_inputs) == len(self.sequence):
            self.round += 1

            if self.round > MAX_ROUND:
                self.finished = True
                if self.mqtt_client:
                    self.mqtt_client.publish_led_off()
            else:
                self.generate_round()

    def is_finished(self):
        return self.finished

    def get_result(self):
        fun_delta = min(30, self.score // 100)

        return {
            "game_type": "memory",
            "score": self.score,
            "fun_delta": fun_delta
        }
