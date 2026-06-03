import random

import pygame


class BlueRedFlagScene:
    def __init__(self, screen, state, sprites, mqtt_client, font_sm, font_md, font_lg):
        self.screen = screen
        self.state = state
        self.sprites = sprites
        self.mqtt_client = mqtt_client
        self.font_sm = font_sm
        self.font_md = font_md
        self.font_lg = font_lg
        self.started_at = pygame.time.get_ticks()
        self.finished = False
        self.score = 0
        self.direction = random.choice(["LEFT", "RIGHT"])

    def draw(self):
        self.screen.fill((73, 116, 181))
        title = self.font_lg.render("청기백기 게임", True, (255, 255, 255))
        guide = self.font_md.render("3초 뒤 자동 결과가 나와요", True, (255, 255, 255))
        self.screen.blit(title, title.get_rect(center=(240, 38)))
        self.screen.blit(guide, guide.get_rect(center=(240, 70)))

        stage = self.state.get("growth_stage", "BABY")
        key = "BLUE_RED_LEFT" if self.direction == "LEFT" else "BLUE_RED_RIGHT"
        sprite = self.sprites.get(stage, {}).get(key)
        if sprite:
            self.screen.blit(sprite, (185, 125))

    def update(self):
        if not self.finished and pygame.time.get_ticks() - self.started_at >= 3000:
            self.finished = True
            self.score = 100

    def is_finished(self):
        return self.finished

    def get_result(self):
        return {
            "game_type": "blue_red_flag",
            "score": self.score,
            "fun_delta": 10,
        }

    def handle_click(self, mx, my):
        return None
