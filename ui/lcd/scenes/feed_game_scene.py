import pygame


class FeedGameScene:
    def __init__(self, screen, state, sprites, food_sprites, font_sm, font_md, font_lg):
        self.screen = screen
        self.state = state
        self.sprites = sprites
        self.food_sprites = food_sprites
        self.font_sm = font_sm
        self.font_md = font_md
        self.font_lg = font_lg
        self.started_at = pygame.time.get_ticks()
        self.finished = False
        self.caught_food_ids = []
        self.hunger_delta = 0
        self.player_x = 210

    def draw(self):
        self.screen.fill((73, 116, 181))
        title = self.font_lg.render("밥 먹기 게임", True, (255, 255, 255))
        guide = self.font_md.render("좌우 방향키로 움직이고 3초 뒤 결과가 나와요", True, (255, 255, 255))
        self.screen.blit(title, title.get_rect(center=(240, 35)))
        self.screen.blit(guide, guide.get_rect(center=(240, 66)))

        stage = self.state.get("growth_stage", "BABY")
        sprite_list = self.sprites.get(stage, {}).get("FEED", [])
        sprite = sprite_list[(pygame.time.get_ticks() // 300) % len(sprite_list)] if sprite_list else None
        if sprite:
            self.screen.blit(sprite, (self.player_x, 170))

        for idx, food in enumerate(self.food_sprites.values()):
            if food:
                self.screen.blit(food, (130 + idx * 85, 110))

    def update(self):
        if not self.finished and pygame.time.get_ticks() - self.started_at >= 3000:
            self.finished = True
            self.caught_food_ids = [1, 2]
            self.hunger_delta = 20

    def move_left(self):
        self.player_x = max(40, self.player_x - 24)

    def move_right(self):
        self.player_x = min(330, self.player_x + 24)

    def is_finished(self):
        return self.finished

    def get_result(self):
        return {
            "hunger_delta": self.hunger_delta,
            "caught_food_ids": self.caught_food_ids,
        }

    def handle_click(self, mx, my):
        return None
