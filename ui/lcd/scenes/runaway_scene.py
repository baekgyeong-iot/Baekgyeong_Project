import pygame

SCREEN_WIDTH = 480
SCREEN_HEIGHT = 320

COLOR_BG = (73, 116, 181)
COLOR_POPUP_BG = (255, 255, 255)
COLOR_POPUP_BORDER = (43, 67, 110)

COLOR_BUTTON = (46, 204, 113)

COLOR_WHITE = (255, 255, 255)
COLOR_BLACK = (0, 0, 0)

class RunawayScene:

    def __init__(
        self,
        screen,
        sprites,
        state,
        font_sm,
        font_md,
        font_lg
    ):
        self.screen = screen
        self.sprites = sprites
        self.state = state

        self.font_sm = font_sm
        self.font_md = font_md
        self.font_lg = font_lg

        self.last_click_time = 0
        self.click_cooldown = 500

        self.restart_button = pygame.Rect(
            145, 250, 190, 46
        )

    # ----------------------------------
    # Draw
    # ----------------------------------

    def draw(self):
        self.screen.fill(COLOR_BG)
        self.draw_character()
        self.draw_popup()

    # ----------------------------------
    # Character
    # ----------------------------------

    def draw_character(self):

        growth_stage = self.state.get(
            "growth_stage",
            "BABY"
        )

        sprite = (
            self.sprites
            .get(growth_stage, {})
            .get("RUNAWAY")
        )

        if sprite is not None:
            rect = sprite.get_rect(center=(240, 90))
            self.screen.blit(sprite, rect)
        else:
            # fallback (스프라이트 없을 때)
            pygame.draw.circle(
                self.screen,
                COLOR_WHITE,
                (240, 90),
                55
            )

    # ----------------------------------
    # Popup
    # ----------------------------------

    def draw_popup(self):

        popup_rect = pygame.Rect(35, 145, 410, 155)

        pygame.draw.rect(
            self.screen,
            COLOR_POPUP_BG,
            popup_rect,
            border_radius=12
        )

        pygame.draw.rect(
            self.screen,
            COLOR_POPUP_BORDER,
            popup_rect,
            3,
            border_radius=12
        )

        title = self.font_lg.render(
            "백경이가 가출했습니다",
            True,
            COLOR_BLACK
        )

        self.screen.blit(
            title,
            title.get_rect(center=(240, 175))
        )

        desc1 = self.font_md.render(
            "외로웠던 백경이가 집을 나갔어요",
            True,
            COLOR_BLACK
        )

        desc2 = self.font_sm.render(
            "다음에는 조금 더 잘 돌봐주세요",
            True,
            COLOR_BLACK
        )

        self.screen.blit(
            desc1,
            desc1.get_rect(center=(240, 205))
        )

        self.screen.blit(
            desc2,
            desc2.get_rect(center=(240, 228))
        )

        pygame.draw.rect(
            self.screen,
            COLOR_BUTTON,
            self.restart_button,
            border_radius=8
        )

        button_text = self.font_md.render(
            "새로 키우기",
            True,
            COLOR_WHITE
        )

        self.screen.blit(
            button_text,
            button_text.get_rect(center=self.restart_button.center)
        )

    # ----------------------------------
    # Click
    # ----------------------------------

    def handle_click(self, mx, my):

        now = pygame.time.get_ticks()

        if (
            now - self.last_click_time
            < self.click_cooldown
        ):
            return None
        
        if self.restart_button.collidepoint(
            mx,
            my
        ):
            self.last_click_time = now

            return "NEW_BAEKGYEONG_REQUESTED"

        return None

    # ----------------------------------
    # System Event
    # ----------------------------------

    def handle_system_event(self, event_name, payload=None):
        # 현재는 단순 씬이라 별도 처리 없음
        pass