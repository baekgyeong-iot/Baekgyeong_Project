#gyro_game_scene.py
# ui/lcd/scenes/gyro_game_scene.py

import pygame


SCREEN_WIDTH = 480
SCREEN_HEIGHT = 320

COLOR_BG = (73, 116, 181)
COLOR_WHITE = (255, 255, 255)
COLOR_YELLOW = (255, 220, 80)


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

        if self.detected:

            success = self.font_md.render(
                f"재미 +{self.fun_delta}",
                True,
                COLOR_YELLOW
            )

            self.screen.blit(
                success,
                success.get_rect(
                    center=(240, 260)
                )
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

        if event != "GYRO_CHANGED":
            return

        direction = payload.get(
            "tilt_direction"
        )

        if direction not in (
            "LEFT",
            "RIGHT",
            "FORWARD",
            "BACKWARD"
        ):
            print(f"[gyro]{direction}")

            self.complete_game()

            return
        
        elif event == "DEVICE_SHAKEN":
            
            shake_power = payload.get(
                "shake_power",
                0
            )

            print(
                f"[shake]power={shake_power}"
            )

            self.complete_game()

    # ----------------------------------
    # Complete
    # ----------------------------------

    def complete_game(self):

        print("[gyro] complete_game()")

        if self.detected:
            return

        self.detected = True

        self.score = 100
        self.fun_delta = 5

        self.state["fun"] = min(
            100,
            self.state.get("fun", 0)
            + self.fun_delta
        )

        pygame.time.set_timer(
            pygame.USEREVENT + 100,
            1200,
            loops=1
        )

    # ----------------------------------
    # Update
    # ----------------------------------

    def update(self):

        pass

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