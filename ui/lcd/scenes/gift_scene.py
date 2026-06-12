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
        font_lg,
        gift_name = "알 수 없는 선물"
    ):

        self.screen = screen
        self.state = state
        self.sprites = sprites

        self.font_md = font_md
        self.font_lg = font_lg
        
        self.gift_name = gift_name

        self.start_time = pygame.time.get_ticks()

        self.duration = 3000

    def update(self):

        self.elapsed = (
            pygame.time.get_ticks()
            - self.start_time
        )

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

        gift_text = self.font_md.render(
            self.gift_name,
            True,
            WHITE
        )

        self.screen.blit(
            gift_text,
            gift_text.get_rect(
                center=(240,260)
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
            .get("PRESENT")
        )

        if sprite is None:
            return

        elapsed = (
            pygame.time.get_ticks()
            - self.start_time
        )

        float_y = int(
            math.sin(
                elapsed * 0.003
            ) * 4
        )

        rect = sprite.get_rect(
        center=(
                SCREEN_WIDTH // 2,
                145 + float_y
            )
        )

        self.screen.blit(
            sprite,
            rect
        )

    def draw_sparkles(self):

        t = pygame.time.get_ticks()

        for i in range(6):

            center_x = SCREEN_WIDTH // 2 - 60

            x = center_x + i * 20

            y = (
                75
                + int(
                    math.sin(
                        t*0.003 + i * 0.7
                    ) * 3
                )
            )

            pygame.draw.circle(
                self.screen,
                YELLOW,
                (x,y),
                4
            )