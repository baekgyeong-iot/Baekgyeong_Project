import pygame


class FeedResultScene:
    def __init__(self, screen, result, font_sm, font_md, font_lg):
        self.screen = screen
        self.result = result or {}
        self.font_sm = font_sm
        self.font_md = font_md
        self.font_lg = font_lg
        self.close_button = pygame.Rect(165, 230, 150, 45)

    def draw(self):
        self.screen.fill((235, 242, 252))
        delta = self.result.get("hunger_delta", 0)
        count = len(self.result.get("caught_food_ids", []))

        title = self.font_lg.render("밥 먹기 완료", True, (30, 30, 30))
        body = self.font_md.render(f"음식 {count}개 / 배고픔 +{delta}", True, (70, 70, 70))

        self.screen.blit(title, title.get_rect(center=(240, 105)))
        self.screen.blit(body, body.get_rect(center=(240, 155)))

        pygame.draw.rect(self.screen, (73, 116, 181), self.close_button, border_radius=10)
        text = self.font_md.render("확인", True, (255, 255, 255))
        self.screen.blit(text, text.get_rect(center=self.close_button.center))

    def handle_click(self, mx, my):
        if self.close_button.collidepoint(mx, my):
            return "FEED_RESULT_CONFIRMED"
        return None
