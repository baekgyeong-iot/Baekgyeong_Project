#blue_red_flag_scene.py
import pygame
import random

SCREEN_WIDTH = 480
SCREEN_HEIGHT = 320

GAME_DURATION = 30

LED_INTERVAL = 1200
POSE_DURATION = 300

COLOR_BG = (73, 116, 181)

COLOR_WHITE = (255, 255, 255)

COLOR_DARK = (32, 55, 88)


class BlueRedFlagScene:

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

        self.score = 0

        self.finished = False

        self.start_time = (
            pygame.time.get_ticks()
        )

        self.last_led_change = (
            pygame.time.get_ticks()
        )

        self.last_input_time = -250

        self.player_pose = "IDLE"

        self.pose_start_time = 0

        self.current_led = (
            random.choice(
                ["LEFT", "RIGHT"]
            )
        )

        self.send_led()

    # --------------------------------
    # LED MQTT
    # --------------------------------

    def send_led(self):

        if not self.mqtt_client:
            return

        if self.current_led == "LEFT":

            self.mqtt_client.publish_led_left()

        else:

            self.mqtt_client.publish_led_right()

    # --------------------------------
    # Update
    # --------------------------------

    def update(self):

        now = pygame.time.get_ticks()

        elapsed = (
            now
            - self.start_time
        ) // 1000

        if elapsed >= GAME_DURATION:

            self.finished = True

            if self.mqtt_client:

                self.mqtt_client.publish_led_off()

            return

        # LED 변경

        if (
            now
            - self.last_led_change
            >= LED_INTERVAL
        ):

            self.current_led = (
                random.choice(
                    ["LEFT", "RIGHT"]
                )
            )

            self.last_led_change = now

            self.send_led()

        # 포즈 복귀

        if (
            self.player_pose != "IDLE"
            and
            now - self.pose_start_time
            >= POSE_DURATION
        ):

            self.player_pose = "IDLE"

    # --------------------------------
    # Draw
    # --------------------------------

    def draw(self):

        self.screen.fill(
            COLOR_BG
        )

        self.draw_header()

        self.draw_led_hint()

        self.draw_character()

        self.draw_button_hint()

    # --------------------------------
    # Header
    # --------------------------------

    def draw_header(self):

        remain = max(

            0,

            GAME_DURATION
            -
            (
                pygame.time.get_ticks()
                -
                self.start_time
            ) // 1000
        )

        score_text = self.font_md.render(
            f"점수 : {self.score}",
            True,
            COLOR_WHITE
        )

        time_text = self.font_md.render(
            f"남은시간 : {remain}",
            True,
            COLOR_WHITE
        )

        self.screen.blit(
            score_text,
            (20, 20)
        )

        self.screen.blit(
            time_text,
            (320, 20)
        )

    # --------------------------------
    # LCD 안내 문구
    # --------------------------------

    def draw_led_hint(self):

        led_text = "LED에 맞춰 버튼을 누르세요"

        text = self.font_md.render(
            led_text,
            True,
            COLOR_WHITE
        )

        self.screen.blit(
            text,
            text.get_rect(center=(SCREEN_WIDTH // 2, 90))
        )

    # --------------------------------
    # Character
    # --------------------------------

    def draw_character(self):

        stage = self.state.get(
            "growth_stage",
            "BABY"
        )

        sprite = None

        if self.player_pose == "LEFT":

            sprite = (
                self.sprites
                .get(stage, {})
                .get(
                    "BLUE_RED_LEFT"
                )
            )

        elif self.player_pose == "RIGHT":

            sprite = (
                self.sprites
                .get(stage, {})
                .get(
                    "BLUE_RED_RIGHT"
                )
            )

        else:

            basic = (
                self.sprites
                .get(stage, {})
                .get(
                    "BASIC",
                    []
                )
            )

            if basic:

                sprite = basic[
                    (
                        pygame.time.get_ticks()
                        // 400
                    )
                    %
                    len(basic)
                ]

        if sprite:

            rect = sprite.get_rect(
                center=(240, 220)
            )

            self.screen.blit(
                sprite,
                rect
            )

    # --------------------------------
    # 물리 버튼 안내
    # --------------------------------

    def draw_button_hint(self):

        pygame.draw.rect(
            self.screen,
            COLOR_DARK,
            pygame.Rect(70, 258, 340, 38),
            border_radius=12
        )

        hint = self.font_sm.render(
            "실제 왼쪽/오른쪽 버튼을 누르세요",
            True,
            COLOR_WHITE
        )

        self.screen.blit(
            hint,
            hint.get_rect(center=(240, 277))
        )

    # --------------------------------
    # 터치 입력 비활성화
    # --------------------------------

    def handle_click(
            self,
            mx,
            my
    ):
        return None

    def handle_short_press(self, direction):
        self.handle_button(direction)
        return None

    # --------------------------------
    # 입력 처리 
    # --------------------------------

    def handle_button(
        self,
        direction
    ):

        now = pygame.time.get_ticks()

        # 연타 방지

        if (
            now
            - self.last_input_time
            < 250
        ):
            return

        self.last_input_time = now

        self.player_pose = (
            direction
        )

        self.pose_start_time = now

        # 정답

        if (
            direction
            ==
            self.current_led
        ):

            self.score += 10

        else:

            self.score = max(
                0,
                self.score - 50
            )

    # --------------------------------
    # 종료 여부
    # --------------------------------

    def is_finished(self):

        return self.finished

    # --------------------------------
    # 결과 반환
    # --------------------------------

    def get_result(self):

        fun_delta = min(
            30,
            self.score // 10
        )

        return {

            "game_type":
                "blue_red_flag",

            "score":
                self.score,

            "fun_delta":
                fun_delta
        }
