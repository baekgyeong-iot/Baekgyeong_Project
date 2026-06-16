#gyro_game_scene.py
# ui/lcd/scenes/gyro_game_scene.py

import pygame


SCREEN_WIDTH = 480
SCREEN_HEIGHT = 320

COLOR_BG = (73, 116, 181)
COLOR_WHITE = (255, 255, 255)
COLOR_YELLOW = (255, 220, 80)
COLOR_DARK = (32, 55, 88)

GAME_DURATION_MS = 15000
RESULT_DELAY_MS = 1200


class GyroGameScene:

    GAME_TYPE = "red_light_green_light"

    def __init__(
        self,
        screen,
        state,
        mqtt_client,
        font_sm,
        font_md,
        font_lg
    ):

        self.screen = screen
        self.state = state
        self.mqtt_client = mqtt_client

        self.font_sm = font_sm
        self.font_md = font_md
        self.font_lg = font_lg

        self.finished = False

        self.score = 0
        self.fun_delta = 0

        self.detected = False
        self.start_time = pygame.time.get_ticks()
        self.result_timer_started = False
        self.last_input_message = ""
        self.last_input_at = 0

    # ----------------------------------
    # Draw
    # ----------------------------------

    def draw(self):

        self.screen.fill(
            COLOR_BG
        )

        title = self.font_lg.render(
            "그냥 놀기",
            True,
            COLOR_WHITE
        )

        self.screen.blit(
            title,
            title.get_rect(
                center=(240, 60)
            )
        )

        pygame.draw.rect(
            self.screen,
            COLOR_WHITE,
            (40, 100, 400, 120),
            border_radius=12
        )

        msg1 = self.font_md.render(
            "LCD를 기울여서",
            True,
            (0, 0, 0)
        )

        msg2 = self.font_md.render(
            "백경이의 재미를 올려주세요!",
            True,
            (0, 0, 0)
        )

        self.screen.blit(
            msg1,
            msg1.get_rect(
                center=(240, 140)
            )
        )

        self.screen.blit(
            msg2,
            msg2.get_rect(
                center=(240, 175)
            )
        )

        score_text = self.font_md.render(
            f"점수 {self.score}",
            True,
            COLOR_YELLOW
        )

        self.screen.blit(
            score_text,
            score_text.get_rect(center=(240, 232))
        )

        if self.detected:

            success = self.font_md.render(
                f"재미 +{self.fun_delta}",
                True,
                COLOR_YELLOW
            )

            self.screen.blit(
                success,
                success.get_rect(
                    center=(240, 268)
                )
            )
        else:

            remain = max(
                0,
                (GAME_DURATION_MS - (pygame.time.get_ticks() - self.start_time))
                // 1000
            )

            time_panel = pygame.Rect(160, 252, 160, 36)

            pygame.draw.rect(
                self.screen,
                COLOR_DARK,
                time_panel,
                border_radius=10
            )

            time_text = self.font_sm.render(
                f"남은 시간 {remain}초",
                True,
                COLOR_WHITE
            )

            self.screen.blit(
                time_text,
                time_text.get_rect(center=time_panel.center)
            )

            if (
                self.last_input_message
                and
                pygame.time.get_ticks() - self.last_input_at < 600
            ):
                input_text = self.font_sm.render(
                    self.last_input_message,
                    True,
                    COLOR_YELLOW
                )

                self.screen.blit(
                    input_text,
                    input_text.get_rect(center=(240, 300))
                )

    # ----------------------------------
    # MQTT Event
    # ----------------------------------

    def handle_system_event(
        self,
        event,
        payload
    ):

        if self.finished:
            return

        if event == "GYRO_CHANGED":
            direction = payload.get("tilt_direction")

            if direction in (
                "LEFT",
                "RIGHT",
                "FORWARD",
                "BACKWARD"
            ):
                print(f"[gyro] direction={direction}")
                self.add_score(
                    10,
                    f"{direction} +10"
                )

            return

        if event == "DEVICE_SHAKEN":
            shake_power = int(
                payload.get(
                    "shake_power",
                    5
                )
            )

            print(
                f"[shake] power={shake_power}"
            )

            self.add_score(
                max(1, shake_power) * 10,
                f"흔들기 +{max(1, shake_power) * 10}"
            )
            return

    # ----------------------------------
    # Score / Complete
    # ----------------------------------

    def add_score(
        self,
        score_delta,
        message
    ):

        if self.detected:
            return

        self.score += max(0, int(score_delta))
        self.fun_delta = min(
            30,
            max(
                1,
                self.score // 20
            )
        )
        self.last_input_message = message
        self.last_input_at = pygame.time.get_ticks()

    def complete_game(self):

        print("[gyro] complete_game()")

        if self.detected:
            return

        self.detected = True
        if self.score <= 0:
            self.fun_delta = 0

        self.start_result_timer()

    def start_result_timer(self):

        if self.result_timer_started:
            return

        self.result_timer_started = True

        pygame.time.set_timer(
            pygame.USEREVENT + 100,
            RESULT_DELAY_MS,
            loops=1
        )

    # ----------------------------------
    # Update
    # ----------------------------------

    def update(self):

        if self.finished or self.detected:
            return

        if pygame.time.get_ticks() - self.start_time >= GAME_DURATION_MS:
            self.complete_game()

    # ----------------------------------
    # Pygame Event
    # ----------------------------------

    def handle_event(
        self,
        event
    ):

        if (
            event.type
            ==
            pygame.USEREVENT + 100
        ):
            print("[gyro] timer received")

            self.finished = True

    # ----------------------------------
    # Result
    # ----------------------------------

    def is_finished(self):

        return self.finished

    def get_result(self):

        return {
            "game_type": self.GAME_TYPE,
            "score": self.score,
            "fun_delta": self.fun_delta
        }
