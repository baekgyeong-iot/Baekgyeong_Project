import pygame

SCREEN_WIDTH = 480
SCREEN_HEIGHT = 320

COLOR_BG = (245, 248, 255)

COLOR_PANEL = (255, 255, 255)
COLOR_BORDER = (73, 116, 181)

COLOR_BUTTON = (73, 116, 181)
COLOR_BUTTON_HOVER = (58, 95, 158)

COLOR_WHITE = (255, 255, 255)

COLOR_BLACK = (30, 30, 30)
COLOR_GRAY = (120, 120, 120)


class PlayResultScene:

    def __init__(
        self,
        screen,
        result,
        font_sm,
        font_md,
        font_lg
    ):

        self.screen = screen
        self.result = result or {}

        self.font_sm = font_sm
        self.font_md = font_md
        self.font_lg = font_lg

        self.panel_rect = pygame.Rect(
            50,
            20,
            380,
            280
        )

        self.ok_button = pygame.Rect(
            165,
            240,
            150,
            45
        )

        self.game_name_map = {
            "blue_red_flag": "청기백기 게임",
            "memory": "암기 게임",
            "red_light_green_light": "무궁화 꽃이 피었습니다"
        }

    # --------------------------------
    # Draw
    # --------------------------------

    def draw(self):

        self.screen.fill(COLOR_BG)

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
            width=4,
            border_radius=18
        )

        self.draw_title()
        self.draw_result()
        self.draw_notice()
        self.draw_button()

    # --------------------------------
    # Title
    # --------------------------------

    def draw_title(self):

        title = self.font_lg.render(
            "게임 결과",
            True,
            COLOR_BLACK
        )

        self.screen.blit(
            title,
            title.get_rect(
                center=(240, 70)
            )
        )

    # --------------------------------
    # Result
    # --------------------------------

    def draw_result(self):

        game_type = self.result.get(
            "game_type",
            ""
        )

        score = self.result.get(
            "score",
            0
        )

        fun_delta = self.result.get(
            "fun_delta",
            0
        )

        game_name = self.game_name_map.get(
            game_type,
            game_type
        )

        lines = [
            f"게임 : {game_name}",
            f"점수 : {score}",
            f"재미 증가 : +{fun_delta}"
        ]

        start_y = 120
        line_gap = 36

        for i, line in enumerate(lines):

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
                        start_y + (i * line_gap)
                    )
                )
            )

    # --------------------------------
    # Notice
    # --------------------------------

    def draw_notice(self):

        notice = self.font_sm.render(
            "랭킹은 대시보드에서 확인할 수 있습니다.",
            True,
            COLOR_GRAY
        )

        self.screen.blit(
            notice,
            notice.get_rect(
                center=(
                    SCREEN_WIDTH // 2,
                    215
                )
            )
        )

    # --------------------------------
    # Button
    # --------------------------------

    def draw_button(self):

        mx, my = pygame.mouse.get_pos()

        button_color = COLOR_BUTTON

        if self.ok_button.collidepoint(mx, my):
            button_color = COLOR_BUTTON_HOVER

        pygame.draw.rect(
            self.screen,
            button_color,
            self.ok_button,
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
                center=self.ok_button.center
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

        if self.ok_button.collidepoint(
            mx,
            my
        ):
            return "PLAY_RESULT_CLOSE"

        return None

    # --------------------------------
    # Update
    # --------------------------------

    def update(self):
        pass