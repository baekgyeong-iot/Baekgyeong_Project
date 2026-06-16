#main_scene.py
import pygame
import math

TOP_BAR_HEIGHT = 56
BOTTOM_BAR_HEIGHT = 50

SCREEN_WIDTH = 480
SCREEN_HEIGHT = 320

CHARACTER_SIZE = 110

CHARACTER_X = (
    SCREEN_WIDTH // 2
    + 50
    - CHARACTER_SIZE // 2
)

CHARACTER_Y = 105

COLOR_TOP_BAR = (43, 67, 110)
COLOR_BOTTOM_BAR = (29, 45, 76)

COLOR_MAIN_BG = (73, 116, 181)
COLOR_LCD_INNER_BORDER = (100, 140, 200)

COLOR_WHITE = (255, 255, 255)
COLOR_YELLOW = (255, 255, 0)

COLOR_BTN_BG = (224, 224, 224)
COLOR_BTN_ACTIVE_BG = (180, 180, 180)
COLOR_BTN_BORDER = (176, 176, 176)
COLOR_SELECTED_BORDER = (255, 255, 255)

COLOR_TEXT_DARK = (17, 17, 17)

COLOR_HEART = (255, 100, 150)


class MainScene:

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

        self.feed_button_rect = pygame.Rect(
            20, 70, 110, 42
        )

        self.sleep_button_rect = pygame.Rect(
            20, 120, 110, 42
        )

        self.play_button_rect = pygame.Rect(
            20, 170, 110, 42
        )

        self.talk_button_rect = pygame.Rect(
            20, 220, 110, 42
        )

        self.character_rect = pygame.Rect(
            CHARACTER_X,
            CHARACTER_Y,
            CHARACTER_SIZE,
            CHARACTER_SIZE
        )

        self.active_button_idx = 0
        self.button_pressed_time = 0

        self.is_bouncing = False
        self.bounce_start_time = 0

        self.show_heart_effect = False
        self.heart_effect_start_time = 0

    # -------------------------
    # Draw
    # -------------------------

    def draw(self):

        self.draw_main_background()

        self.draw_top_status_bar()

        self.draw_character()

        self.draw_buttons()

        self.draw_dialogue_box()

        self.draw_heart_effect()

    # -------------------------
    # Background
    # -------------------------

    def draw_main_background(self):

        pygame.draw.rect(
            self.screen,
            COLOR_MAIN_BG,
            (
                0,
                TOP_BAR_HEIGHT,
                SCREEN_WIDTH,
                SCREEN_HEIGHT - TOP_BAR_HEIGHT
            )
        )

        pygame.draw.rect(
            self.screen,
            COLOR_LCD_INNER_BORDER,
            (
                0,
                TOP_BAR_HEIGHT,
                SCREEN_WIDTH,
                SCREEN_HEIGHT - TOP_BAR_HEIGHT
            ),
            4
        )

    # -------------------------
    # Status Bar
    # -------------------------

    def draw_top_status_bar(self):

        pygame.draw.rect(
            self.screen,
            COLOR_TOP_BAR,
            (0, 0, SCREEN_WIDTH, TOP_BAR_HEIGHT)
        )

        stat_list = [

            ("hunger", "hunger"),

            ("energy", "energy"),

            ("fun", "fun"),

            ("favorability", "favorability")
        ]

        col_width = SCREEN_WIDTH // 4

        for i, (state_key, icon_key) in enumerate(
            stat_list
        ):

            value = self.state.get(
                state_key,
                0
            )

            start_x = (
                i * col_width + 10
            )

            icon = self.icons.get(
                icon_key
            )

            if icon:

                self.screen.blit(
                    icon,
                    (start_x, 8)
                )

            text = self.font_md.render(
                f"{value}%",
                True,
                COLOR_WHITE
            )

            self.screen.blit(
                text,
                (start_x + 45, 16)
            )

    # -------------------------
    # Character
    # -------------------------

    def draw_character(self):

        if self.state.get(
            "is_runaway",
            False
        ):
            return

        stage = self.state.get(
            "growth_stage",
            "BABY"
        )

        current_time = (
            pygame.time.get_ticks()
        )

        frame_idx = (
            current_time // 400
        ) % 2

        sprite_list = (
            self.sprites
            .get(stage, {})
            .get("BASIC", [])
        )

        sprite = None

        if len(sprite_list) > frame_idx:

            sprite = sprite_list[
                frame_idx
            ]

        offset_y = 0

        if self.is_bouncing:

            elapsed = (
                current_time
                - self.bounce_start_time
            )

            if elapsed < 700:

                offset_y = int(
                    -12 *
                    math.sin(
                        elapsed * 0.02
                    )
                )

            else:

                self.is_bouncing = False

        if sprite:

            self.screen.blit(
                sprite,
                (
                    CHARACTER_X,
                    CHARACTER_Y + offset_y
                )
            )

    # -------------------------
    # Buttons
    # -------------------------

    def draw_buttons(self):

        labels = [
            "밥 주기",
            "잠 자기",
            "놀 기",
            "대 화",
            "백경이"
        ]

        rects = [
            self.feed_button_rect,
            self.sleep_button_rect,
            self.play_button_rect,
            self.talk_button_rect,
            self.character_rect
        ]

        for idx, rect in enumerate(rects):

            if idx == 4:
                if idx == self.active_button_idx:
                    pygame.draw.rect(
                        self.screen,
                        COLOR_SELECTED_BORDER,
                        rect.inflate(12, 12),
                        4,
                        border_radius=18
                    )
                continue

            color = (

                COLOR_BTN_ACTIVE_BG

                if idx == self.active_button_idx

                else COLOR_BTN_BG
            )

            pygame.draw.rect(
                self.screen,
                color,
                rect,
                border_radius=12
            )

            pygame.draw.rect(
                self.screen,
                COLOR_SELECTED_BORDER if idx == self.active_button_idx else COLOR_BTN_BORDER,
                rect,
                4 if idx == self.active_button_idx else 2,
                border_radius=12
            )

            text = self.font_md.render(
                labels[idx],
                True,
                COLOR_TEXT_DARK
            )

            self.screen.blit(
                text,
                text.get_rect(
                    center=rect.center
                )
            )

    # -------------------------
    # Dialogue
    # -------------------------

    def draw_dialogue_box(self):

        pygame.draw.rect(
            self.screen,
            COLOR_BOTTOM_BAR,
            (
                0,
                SCREEN_HEIGHT
                - BOTTOM_BAR_HEIGHT,
                SCREEN_WIDTH,
                BOTTOM_BAR_HEIGHT
            )
        )

        msg = self.state.get(
            "current_message",
            "백경이와 즐거운 시간을 보내세요."
        )

        if len(msg) > 28:

            msg = msg[:28] + "..."

        text = self.font_md.render(
            msg,
            True,
            COLOR_YELLOW
        )

        self.screen.blit(
            text,
            text.get_rect(
                center=(
                    SCREEN_WIDTH // 2,
                    SCREEN_HEIGHT - 25
                )
            )
        )
    
    def play_stroke_success_animation(self):

        self.is_bouncing = True

        self.bounce_start_time = (
            pygame.time.get_ticks()
        )

        self.show_heart_effect = True

        self.heart_effect_start_time = (
            pygame.time.get_ticks()
        )

    # -------------------------
    # Heart Effect
    # -------------------------

    def draw_heart_effect(self):

        if not self.show_heart_effect:
            return

        elapsed = (
            pygame.time.get_ticks()
            - self.heart_effect_start_time
        )

        if elapsed > 1000:

            self.show_heart_effect = False
            return

        heart = self.font_lg.render(
            "♥",
            True,
            COLOR_HEART
        )

        self.screen.blit(
            heart,
            (
                CHARACTER_X + 80,
                CHARACTER_Y - 20
            )
        )

    # -------------------------
    # Click
    # -------------------------

    def move_selection(self, direction):
        if direction == "LEFT":
            self.active_button_idx = (self.active_button_idx - 1) % 5
        else:
            self.active_button_idx = (self.active_button_idx + 1) % 5

    def confirm_selection(self):
        events = [
            "FEED_BUTTON_CLICKED",
            "SLEEP_BUTTON_CLICKED",
            "PLAY_BUTTON_CLICKED",
            "TEXT_BUTTON_CLICKED",
            "STROKE_ATTEMPT",
        ]
        return events[self.active_button_idx]

    def handle_click(self, mx, my):

        if self.feed_button_rect.collidepoint(
            mx,
            my
        ):

            self.active_button_idx = 0
            self.button_pressed_time = pygame.time.get_ticks()

            return self.confirm_selection()

        if self.sleep_button_rect.collidepoint(
            mx,
            my
        ):

            self.active_button_idx = 1
            self.button_pressed_time = pygame.time.get_ticks()

            return self.confirm_selection()

        if self.play_button_rect.collidepoint(
            mx,
            my
        ):

            self.active_button_idx = 2
            self.button_pressed_time = pygame.time.get_ticks()

            return self.confirm_selection()

        if self.talk_button_rect.collidepoint(
            mx,
            my
        ):

            self.active_button_idx = 3
            self.button_pressed_time = pygame.time.get_ticks()

            return self.confirm_selection()

        if self.character_rect.collidepoint(
            mx,
            my
        ):
            self.active_button_idx = 4
            return self.confirm_selection()

        return None
