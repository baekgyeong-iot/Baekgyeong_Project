import pygame

SCREEN_WIDTH = 480
SCREEN_HEIGHT = 320

COLOR_BG = (
    73,
    116,
    181
)

COLOR_PANEL = (
    255,
    255,
    255
)

COLOR_BORDER = (
    43,
    67,
    110
)
COLOR_SELECTED_BORDER = (255, 255, 255)

COLOR_BUTTON = (
    224,
    224,
    224
)

COLOR_BUTTON_ACTIVE = (
    180,
    180,
    180
)

COLOR_TEXT = (
    17,
    17,
    17
)

COLOR_TITLE = (
    255,
    255,
    255
)


class PlayGameSelectScene:

    def __init__(
        self,
        screen,
        font_sm,
        font_md,
        font_lg
    ):

        self.screen = screen

        self.font_sm = font_sm
        self.font_md = font_md
        self.font_lg = font_lg

        self.selected_idx = 0
        self.button_pressed_time = 0

        self.last_click_time = 0
        self.input_lock_time = 350

        self.blue_red_button = pygame.Rect(
            90,
            80,
            300,
            50
        )

        self.memory_button = pygame.Rect(
            90,
            145,
            300,
            50
        )

        self.free_play_button = pygame.Rect(
            90,
            210,
            300,
            50
        )

    # -------------------------
    # Draw
    # -------------------------

    def draw(self):

        self.screen.fill(
            COLOR_BG
        )

        self.draw_title()

        self.draw_buttons()

    # -------------------------
    # Title
    # -------------------------

    def draw_title(self):

        title = self.font_lg.render(
            "원하는 게임을 선택하세요",
            True,
            COLOR_TITLE
        )

        self.screen.blit(
            title,
            title.get_rect(
                center=(240, 35)
            )
        )

    # -------------------------
    # Buttons
    # -------------------------

    def draw_buttons(self):

        rects = [
            self.blue_red_button,
            self.memory_button,
            self.free_play_button
        ]

        labels = [
            "청기백기 게임",
            "암기 게임",
            "그냥 놀기"
        ]

        for idx, rect in enumerate(rects):

            color = (
                COLOR_BUTTON_ACTIVE
                if idx == self.selected_idx
                else COLOR_BUTTON
            )

            pygame.draw.rect(
                self.screen,
                color,
                rect,
                border_radius=12
            )

            pygame.draw.rect(
                self.screen,
                COLOR_SELECTED_BORDER if idx == self.selected_idx else COLOR_BORDER,
                rect,
                4 if idx == self.selected_idx else 2,
                border_radius=12
            )

            text = self.font_md.render(
                labels[idx],
                True,
                COLOR_TEXT
            )

            self.screen.blit(
                text,
                text.get_rect(
                    center = rect.center
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
        now = pygame.time.get_ticks()

        if now - self.last_click_time < self.input_lock_time:
            return None

        if self.blue_red_button.collidepoint(
            mx,
            my
        ):

            self.selected_idx = 0
            self.button_pressed_time = now
            self.last_click_time = now

            return {
                "event": "PLAY_GAME_SELECTED",
                "payload": {
                    "game_type":
                    "blue_red_flag"
                }
            }

        if self.memory_button.collidepoint(
            mx,
            my
        ):

            self.selected_idx = 1
            self.button_pressed_time = now
            self.last_click_time = now

            return {
                "event": "PLAY_GAME_SELECTED",
                "payload": {
                    "game_type":
                    "memory"
                }
            }

        if self.free_play_button.collidepoint(
            mx,
            my
        ):

            self.selected_idx = 2
            self.button_pressed_time = now
            self.last_click_time = now

            return {
                "event": "PLAY_GAME_SELECTED",
                "payload": {
                    "game_type":
                    "red_light_green_light"
                }
            }

        return None

    def move_selection(self, direction):
        if direction == "LEFT":
            self.selected_idx = (self.selected_idx - 1) % 3
        else:
            self.selected_idx = (self.selected_idx + 1) % 3

    def confirm_selection(self):
        game_types = [
            "blue_red_flag",
            "memory",
            "red_light_green_light"
        ]
        return {
            "event": "PLAY_GAME_SELECTED",
            "payload": {
                "game_type": game_types[self.selected_idx]
            }
        }
