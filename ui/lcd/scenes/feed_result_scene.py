import pygame

SCREEN_WIDTH = 480
SCREEN_HEIGHT = 320

COLOR_BG = (73, 116, 181)

COLOR_PANEL = (255, 255, 255)
COLOR_BORDER = (55, 88, 145)

COLOR_BLACK = (30, 30, 30)
COLOR_GRAY = (100, 100, 100)

COLOR_BUTTON = (73, 116, 181)

COLOR_WHITE = (255, 255, 255)


class FeedResultScene:

    def __init__(
        self,
        screen,
        result,
        font_sm,
        font_md,
        font_lg
    ):

        self.screen = screen

        self.result = result

        self.font_sm = font_sm
        self.font_md = font_md
        self.font_lg = font_lg

        self.food_count = len(
            result["caught_food_ids"]
        )

        self.hunger_gain = (
            result["hunger_delta"]
        )

        # --------------------
        # 중앙 결과 패널
        # --------------------

        self.panel_rect = pygame.Rect(
            70,
            30,
            340,
            260
        )

        # --------------------
        # 확인 버튼
        # --------------------

        self.confirm_rect = pygame.Rect(
            165,
            220,
            150,
            45
        )

    # --------------------------------
    # Draw
    # --------------------------------

    def draw(self):

        self.screen.fill(
            COLOR_BG
        )

        pygame.draw.rect(
            self.screen,
            COLOR_PANEL,
            self.panel_rect,
            border_radius=18
        )

        pygame.draw.rect(
            self.screen,
            COLOR_BORDER,
            self.panel_rect,
            width=3,
            border_radius=18
        )

        self.draw_title()
        self.draw_result()
        self.draw_button()

    # --------------------------------
    # Title
    # --------------------------------

    def draw_title(self):

        title = self.font_lg.render(
            "GAME RESULT",
            True,
            COLOR_BLACK
        )

        self.screen.blit(
            title,
            title.get_rect(
                center=(
                    SCREEN_WIDTH // 2,
                    75
                )
            )
        )

    # --------------------------------
    # Result
    # --------------------------------

    def draw_result(self):

        result_lines = [

            f"먹은 음식 : {self.food_count}개",

            f"배고픔 +{self.hunger_gain}"
        ]

        start_y = 135
        gap = 55

        for i, line in enumerate(result_lines):

            text = self.font_md.render(
                line,
                True,
                COLOR_BLACK
            )

            self.screen.blit(
                text,
                text.get_rect(
                    center=(
                        SCREEN_WIDTH // 2,
                        start_y + (i * gap)
                    )
                )
            )

    # --------------------------------
    # Button
    # --------------------------------

    def draw_button(self):

        pygame.draw.rect(
            self.screen,
            COLOR_BUTTON,
            self.confirm_rect,
            border_radius=10
        )

        text = self.font_md.render(
            "확인",
            True,
            COLOR_WHITE
        )

        self.screen.blit(
            text,
            text.get_rect(
                center = self.confirm_rect.center
            )
        )

    # --------------------------------
    # Click
    # --------------------------------

    def handle_click(
        self,
        mx,
        my
    ):

        if self.confirm_rect.collidepoint(
            mx,
            my
        ):

            return (
                "FEED_RESULT_CONFIRMED"
            )

        return None