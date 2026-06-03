# sleep_scene.py
# scenes/sleep_scene.py

import pygame

SCREEN_WIDTH = 480
SCREEN_HEIGHT = 320

COLOR_BG = (
    73,
    116,
    181
)

COLOR_TEXT = (
    255,
    255,
    255
)

COLOR_PANEL = (
    43,
    67,
    110
)


class SleepScene:

    def __init__(
        self,
        screen,
        state,
        sprites,
        font_sm,
        font_md,
        font_lg
    ):

        self.screen = screen

        self.state = state

        self.sprites = sprites

        self.font_sm = font_sm
        self.font_md = font_md
        self.font_lg = font_lg

    # -------------------------
    # Draw
    # -------------------------

    def draw(self):

        self.screen.fill(
            COLOR_BG
        )

        self.draw_title()

        self.draw_sleep_sprite()

        self.draw_energy()

        self.draw_message()

    # -------------------------
    # Title
    # -------------------------

    def draw_title(self):

        text = self.font_lg.render(
            "백경이 수면중",
            True,
            COLOR_TEXT
        )

        self.screen.blit(
            text,
            text.get_rect(
                center=(240, 30)
            )
        )

    # -------------------------
    # Character
    # -------------------------

    def draw_sleep_sprite(self):

        stage = self.state.get(
            "growth_stage",
            "BABY"
        )

        sprite = (
            self.sprites
            .get(stage, {})
            .get("SLEEP")
        )

        if sprite:

            rect = sprite.get_rect(
                center=(240, 130)
            )

            self.screen.blit(
                sprite,
                rect
            )

        else:

            pygame.draw.circle(
                self.screen,
                COLOR_TEXT,
                (240, 130),
                50
            )

    # -------------------------
    # Energy
    # -------------------------

    def draw_energy(self):

        panel = pygame.Rect(
            140,
            200,
            200,
            50
        )

        pygame.draw.rect(
            self.screen,
            COLOR_PANEL,
            panel,
            border_radius=10
        )

        energy = self.state.get(
            "energy",
            0
        )

        text = self.font_md.render(
            f"에너지 : {energy}%",
            True,
            COLOR_TEXT
        )

        self.screen.blit(
            text,
            text.get_rect(
                center=panel.center
            )
        )

    # -------------------------
    # Message
    # -------------------------

    def draw_message(self):

        text = self.font_sm.render(
            "밝아지면 자동으로 깨어납니다",
            True,
            COLOR_TEXT
        )

        self.screen.blit(
            text,
            text.get_rect(
                center=(240, 290)
            )
        )

    # -------------------------
    # Click
    # -------------------------

    def handle_click(
        self,
        mx,
        my
    ):

        return None