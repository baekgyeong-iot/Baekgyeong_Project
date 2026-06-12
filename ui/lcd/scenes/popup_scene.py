import pygame

SCREEN_WIDTH = 480
SCREEN_HEIGHT = 320

COLOR_OVERLAY = (0, 0, 0)

COLOR_POPUP_BG = (255, 255, 255)
COLOR_POPUP_BORDER = (43, 67, 110)

COLOR_BUTTON = (73, 116, 181)
COLOR_BUTTON_ACTIVE = (55, 90, 150)

COLOR_WHITE = (255, 255, 255)
COLOR_BLACK = (0, 0, 0)

class PopupScene:

    def __init__(
        self,
        screen,
        message,
        font_sm=None,
        font_md=None,
        font_lg=None,
        popup_type = "normal",
        evolution_sprite = None
    ):

        self.screen = screen
        self.message = message

        self.popup_type = popup_type
        self.evolution_sprite = evolution_sprite

        self.last_click_time = 0
        self.click_cooldown = 300

        self.font_sm = font_sm or pygame.font.SysFont(
            "malgungothic",
            16,
            bold=True
        )

        self.font_md = font_md or pygame.font.SysFont(
            "malgungothic",
            20,
            bold=True
        )

        self.font_lg = font_lg or pygame.font.SysFont(
            "malgungothic",
            24,
            bold=True
        )

        popup_width = 340
        popup_height = 180

        self.popup_rect = pygame.Rect(
            (SCREEN_WIDTH - popup_width) // 2,
            (SCREEN_HEIGHT - popup_height) // 2,
            popup_width,
            popup_height
        )

        self.ok_button = pygame.Rect(
            self.popup_rect.centerx - 50,
            self.popup_rect.bottom - 50,
            100,
            36
        )

        self.button_pressed_time = 0

    # --------------------------------
    # Draw
    # --------------------------------

    def draw(self):

        overlay = pygame.Surface(
            (SCREEN_WIDTH, SCREEN_HEIGHT)
        )

        overlay.set_alpha(120)

        overlay.fill(
            COLOR_OVERLAY
        )

        self.screen.blit(
            overlay,
            (0, 0)
        )

        pygame.draw.rect(
            self.screen,
            COLOR_POPUP_BG,
            self.popup_rect,
            border_radius=16
        )

        pygame.draw.rect(
            self.screen,
            COLOR_POPUP_BORDER,
            self.popup_rect,
            3,
            border_radius=16
        )

        if self.popup_type == "evolution":

            self.draw_evolution()

        else:

            self.draw_message()
        
        self.draw_button()

    # --------------------------------
    # Evolution Popup
    # --------------------------------

    def draw_evolution(self):

        title = self.font_lg.render(
            "백경이가 성장했어요!",
            True,
            COLOR_BLACK
        )

        self.screen.blit(
            title,
            title.get_rect(
                center=(
                    self.popup_rect.centerx,
                    self.popup_rect.top + 35
                )
            )
        )

        if self.evolution_sprite:

            sprite_rect = (
                self.evolution_sprite.get_rect(
                    center=(
                        self.popup_rect.centerx,
                        self.popup_rect.centery
                    )
                )
            )

            self.screen.blit(
                self.evolution_sprite,
                sprite_rect
            )

        text = self.font_md.render(
            self.message,
            True,
            COLOR_BLACK
        )

        self.screen.blit(
            text,
            text.get_rect(
                center=(
                    self.popup_rect.centerx,
                    self.popup_rect.bottom - 90
                )
            )
        )


    # --------------------------------
    # Message
    # --------------------------------

    def draw_message(self):

        lines = self.message.split("\n")

        start_y = (
            self.popup_rect.top + 40
        )

        for line in lines:

            text = self.font_md.render(
                line,
                True,
                COLOR_BLACK
            )

            self.screen.blit(
                text,
                text.get_rect(
                    center=(
                        self.popup_rect.centerx,
                        start_y
                    )
                )
            )

            start_y += 32

    # --------------------------------
    # Button
    # --------------------------------

    def draw_button(self):

        now = pygame.time.get_ticks()

        color = COLOR_BUTTON

        if (
            now
            - self.button_pressed_time
            < 150
        ):
            color = COLOR_BUTTON_ACTIVE

        pygame.draw.rect(
            self.screen,
            color,
            self.ok_button,
            border_radius=8
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
        now = pygame.time.get_ticks()

        if (
            now - self.last_click_time
            < self.click_cooldown
        ):
            return None

        if self.ok_button.collidepoint(
            mx,
            my
        ):
            self.last_click_time = now

            self.button_pressed_time = now

            if self.popup_type == "evolution":

                return "EVOLUTION_CONFIRMED"

            return "POPUP_CLOSE"

        return None