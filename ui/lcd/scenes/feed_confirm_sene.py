# scenes/feed_confirm_scene.py

import pygame

COLOR_BG = (235, 242, 252)

COLOR_POPUP_BG = (255, 255, 255)
COLOR_POPUP_BORDER = (73, 116, 181)

COLOR_SHADOW = (180, 190, 210)

COLOR_GREEN = (52, 199, 89)
COLOR_GREEN_HOVER = (40, 170, 72)

COLOR_RED = (255, 95, 86)
COLOR_RED_HOVER = (230, 70, 60)

COLOR_WHITE = (255, 255, 255)
COLOR_BLACK = (30, 30, 30)
COLOR_GRAY = (110, 110, 110)


class FeedConfirmScene:

    def __init__(
        self,
        screen,
        state,
        sprites,
        icons,
        font_sm,
        font_md,
        font_lg
    ):

        self.screen = screen

        self.state = state
        self.sprites = sprites
        self.icons = icons

        self.font_sm = font_sm
        self.font_md = font_md
        self.font_lg = font_lg

        self.popup_rect = pygame.Rect(
            90,
            65,
            300,
            190
        )

        self.confirm_button = pygame.Rect(
            125,
            185,
            100,
            45
        )

        self.cancel_button = pygame.Rect(
            255,
            185,
            100,
            45
        )

    # --------------------------
    # Draw
    # --------------------------

    def draw(self):

        self.screen.fill(
            COLOR_BG
        )

        self.draw_popup()

        self.draw_title()

        self.draw_message()

        self.draw_buttons()

    # --------------------------
    # Popup
    # --------------------------

    def draw_popup(self):

        shadow_rect = self.popup_rect.move(
            5,
            5
        )

        pygame.draw.rect(
            self.screen,
            COLOR_SHADOW,
            shadow_rect,
            border_radius=18
        )

        pygame.draw.rect(
            self.screen,
            COLOR_POPUP_BG,
            self.popup_rect,
            border_radius=18
        )

        pygame.draw.rect(
            self.screen,
            COLOR_POPUP_BORDER,
            self.popup_rect,
            width=3,
            border_radius=18
        )

    # --------------------------
    # Title
    # --------------------------

    def draw_title(self):

        title = self.font_lg.render(
            "밥 먹기 게임",
            True,
            COLOR_BLACK
        )

        self.screen.blit(
            title,
            title.get_rect(
                center=(
                    self.popup_rect.centerx,
                    105
                )
            )
        )

    # --------------------------
    # Message
    # --------------------------

    def draw_message(self):

        text = self.font_md.render(
            "밥 먹기 게임을 시작할까요?",
            True,
            COLOR_GRAY
        )

        self.screen.blit(
            text,
            text.get_rect(
                center=(
                    self.popup_rect.centerx,
                    145
                )
            )
        )

    # --------------------------
    # Buttons
    # --------------------------

    def draw_buttons(self):

        mx, my = pygame.mouse.get_pos()

        start_color = COLOR_GREEN
        cancel_color = COLOR_RED

        if self.confirm_button.collidepoint(
            mx,
            my
        ):
            start_color = COLOR_GREEN_HOVER

        if self.cancel_button.collidepoint(
            mx,
            my
        ):
            cancel_color = COLOR_RED_HOVER

        pygame.draw.rect(
            self.screen,
            start_color,
            self.confirm_button,
            border_radius=10
        )

        pygame.draw.rect(
            self.screen,
            cancel_color,
            self.cancel_button,
            border_radius=10
        )

        start_text = self.font_md.render(
            "시작",
            True,
            COLOR_WHITE
        )

        cancel_text = self.font_md.render(
            "취소",
            True,
            COLOR_WHITE
        )

        self.screen.blit(
            start_text,
            start_text.get_rect(
                center=self.confirm_button.center
            )
        )

        self.screen.blit(
            cancel_text,
            cancel_text.get_rect(
                center=self.cancel_button.center
            )
        )

    # --------------------------
    # Click
    # --------------------------

    def handle_click(
        self,
        mx,
        my
    ):

        if self.confirm_button.collidepoint(
            mx,
            my
        ):
            return "FEED_CONFIRMED"

        if self.cancel_button.collidepoint(
            mx,
            my
        ):
            return "FEED_CANCELLED"

        return None