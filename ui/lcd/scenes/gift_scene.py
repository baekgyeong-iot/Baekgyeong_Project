import pygame
import math

SCREEN_WIDTH = 480
SCREEN_HEIGHT = 320

BG_COLOR = (73,116,181)
WHITE = (255,255,255)
YELLOW = (255,230,80)

class GiftScene:

    def __init__(
        self,
        screen,
        state,
        sprites,
        font_md,
        font_lg
    ):

        self.screen = screen
        self.state = state
        self.sprites = sprites

        self.font_md = font_md
        self.font_lg = font_lg

        self.start_time = pygame.time.get_ticks()

        self.duration = 2500

    def update(self):

        pass

    def is_finished(self):

        return (
            pygame.time.get_ticks()
            - self.start_time
            > self.duration
        )

    def draw(self):

        self.screen.fill(BG_COLOR)

        title = self.font_lg.render(
            "선물을 가져왔어요!",
            True,
            WHITE
        )

        self.screen.blit(
            title,
            title.get_rect(
                center=(240,40)
            )
        )

        self.draw_gift_sprite()

        self.draw_sparkles()

    def draw_gift_sprite(self):

        stage = self.state.get(
            "growth_stage",
            "BABY"
        )

        sprite = (
            self.sprites
            .get(stage,{})
            .get("GIFT")
        )

        if sprite is None:
            return

        elapsed = (
            pygame.time.get_ticks()
            - self.start_time
        )

        shake_x = int(
            math.sin(
                elapsed * 0.04
            ) * 8
        )

        self.screen.blit(
            sprite,
            (
                180 + shake_x,
                90
            )
        )

    def draw_sparkles(self):

        t = pygame.time.get_ticks()

        for i in range(6):

            x = 180 + i*25

            y = (
                70
                + int(
                    math.sin(
                        t*0.01+i
                    ) * 10
                )
            )

            pygame.draw.circle(
                self.screen,
                YELLOW,
                (x,y),
                4
            )