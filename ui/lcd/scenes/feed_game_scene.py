# scenes/feed_game_scene.py

import pygame
import random

from data.food_data import FOOD_LIST


SCREEN_WIDTH = 480
SCREEN_HEIGHT = 320

PLAYER_Y = 140

GAME_TIME = 30000

PLAYER_WIDTH = 110
PLAYER_HEIGHT = 110

FOOD_SIZE = 48

MOVE_SPEED = 20


class FeedGameScene:

    def __init__(
        self,
        screen,
        state,
        sprites,
        food_sprites,
        font_sm,
        font_md,
        font_lg
    ):

        self.screen = screen
        self.state = state

        self.sprites = sprites
        self.food_sprites = food_sprites

        self.font_sm = font_sm
        self.font_md = font_md
        self.font_lg = font_lg

        self.stage = state.get(
            "growth_stage",
            "BABY"
        )

        self.player_x = (
            SCREEN_WIDTH // 2
            - PLAYER_WIDTH // 2
        )

        # 터치 버튼
        self.left_button_rect = pygame.Rect(
            20,
            260,
            200,
            50
        )

        self.right_button_rect = pygame.Rect(
            260,
            260,
            200,
            50
        )

        self.direction = "CENTER"

        self.foods = []

        self.caught_food_ids = []

        self.total_hunger_gain = 0

        self.start_time = pygame.time.get_ticks()

        self.last_spawn_time = 0

        # 음식 생성 주기 랜덤
        self.spawn_interval = random.randint(
            500,
            1500
        )

    # -----------------
    # update
    # -----------------

    def update(self):

        current_time = pygame.time.get_ticks()

        if (
            current_time
            - self.last_spawn_time
            > self.spawn_interval
        ):

            self.spawn_food()

            self.last_spawn_time = current_time

            self.spawn_interval = random.randint(
                500,
                1500
            )

        self.update_foods()

    # -----------------
    # 음식 생성
    # -----------------

    def spawn_food(self):

        food_data = random.choice(
            FOOD_LIST
        )

        sprite = self.food_sprites.get(
            food_data["sprite"]
        )

        print(
            f"[SPAWN] "
            f"{food_data['name']} "
            f"sprite={food_data['sprite']}"
        )

        self.foods.append(
            {
                "food_id":
                    food_data["food_id"],

                "name":
                    food_data["name"],

                "sprite":
                    sprite,

                "hunger_value":
                    food_data["hunger_value"],

                # 화면 전체에서 랜덤 생성
                "x":
                    random.randint(
                        0,
                        SCREEN_WIDTH - FOOD_SIZE
                    ),

                "y":
                    -FOOD_SIZE,

                # 속도 랜덤
                "speed":
                    random.randint(
                        2,
                        8
                    )
            }
        )

    # -----------------
    # 음식 이동
    # -----------------

    def update_foods(self):

        player_rect = pygame.Rect(
            self.player_x,
            PLAYER_Y,
            PLAYER_WIDTH,
            PLAYER_HEIGHT
        )

        remove_list = []

        for food in self.foods:

            food["y"] += food["speed"]

            food_rect = pygame.Rect(
                food["x"],
                food["y"],
                FOOD_SIZE,
                FOOD_SIZE
            )

            if player_rect.colliderect(
                food_rect
            ):

                self.total_hunger_gain += (
                    food["hunger_value"]
                )

                self.caught_food_ids.append(
                    food["food_id"]
                )

                print(
                    f"FOOD_CAUGHT : "
                    f"{food['name']}"
                )

                remove_list.append(
                    food
                )

            elif food["y"] > SCREEN_HEIGHT:

                remove_list.append(
                    food
                )

        for food in remove_list:

            if food in self.foods:

                self.foods.remove(
                    food
                )

    # -----------------
    # 터치 버튼
    # ----------------- 

    def draw_touch_buttons(self):

        pygame.draw.rect(
            self.screen,
            (70,120,255),
            self.left_button_rect,
            border_radius=12
        )

        pygame.draw.rect(
            self.screen,
            (255,255,255),
            self.left_button_rect,
            3,
            border_radius=12
        )

        pygame.draw.rect(
            self.screen,
            (255,255,255),
            self.right_button_rect,
            3,
            border_radius=12
        )

        left_text = self.font_md.render(
            "◀ 왼쪽",
            True,
            (255,255,255)
        )

        right_text = self.font_md.render(
            "오른쪽 ▶",
            True,
            (255,255,255)
        )

        self.screen.blit(
            left_text,
            left_text.get_rect(
                center = self.left_button_rect.center
            )
        )

        self.screen.blit(
            right_text,
            right_text.get_rect(
                center = self.right_button_rect.center
            )
        )

    # -----------------
    # draw
    # -----------------

    def draw(self):

        self.screen.fill(
            (73, 116, 181)
        )

        self.draw_ui()

        self.draw_foods()

        self.draw_player()

        self.draw_touch_buttons()

    # -----------------
    # UI
    # -----------------

    def draw_ui(self):

        remain = max(
            0,
            GAME_TIME
            - (
                pygame.time.get_ticks()
                - self.start_time
            )
        )

        sec = remain // 1000

        timer_text = self.font_md.render(
            f"TIME {sec}",
            True,
            (255, 255, 255)
        )

        self.screen.blit(
            timer_text,
            (20, 20)
        )

        score_text = self.font_md.render(
            f"SCORE {self.total_hunger_gain}",
            True,
            (255, 255, 255)
        )

        self.screen.blit(
            score_text,
            (20,50)
        )

    # -----------------
    # 음식 그리기
    # -----------------

    def draw_foods(self):

        for food in self.foods:

            sprite = food["sprite"]

            if sprite is None:

                print(
                    "[ERROR] sprite None :",
                    food["name"]
                )

                continue

            self.screen.blit(
                sprite,
                (
                    food["x"],
                    food["y"]
                )
            )

    # -----------------
    # 플레이어
    # -----------------

    def draw_player(self):

        ticks = (
            pygame.time.get_ticks()
            // 250
        ) % 2

        stage_sprites = self.sprites[
            self.stage
        ]

        if self.direction == "LEFT":

            sprite = stage_sprites[
                "LEFT"
            ][ticks]

        elif self.direction == "RIGHT":

            sprite = stage_sprites[
                "RIGHT"
            ][ticks]

        else:

            sprite = stage_sprites[
                "FEED"
            ][ticks]

        if sprite:

            self.screen.blit(
                sprite,
                (
                    self.player_x,
                    PLAYER_Y
                )
            )

    # -----------------
    # 이동
    # -----------------

    def move_left(self):

        self.direction = "LEFT"

        self.player_x -= MOVE_SPEED

        # 화면 왼쪽 끝
        if self.player_x < 0:

            self.player_x = 0

    def move_right(self):

        self.direction = "RIGHT"

        self.player_x += MOVE_SPEED

        # 화면 오른쪽 끝
        max_x = (
            SCREEN_WIDTH
            - PLAYER_WIDTH
        )

        if self.player_x > max_x:

            self.player_x = max_x

    # -----------------
    # 종료
    # -----------------

    def is_finished(self):

        elapsed = (
            pygame.time.get_ticks()
            - self.start_time
        )

        return elapsed >= GAME_TIME

    # -----------------
    # 결과
    # -----------------

    def get_result(self):

        return {

            "caught_food_ids":
                self.caught_food_ids,

            "hunger_delta":
                max(
                    1,
                    self.total_hunger_gain // 5
                )
        }

    # -----------------
    # 클릭 무시
    # -----------------

    def handle_click(
        self,
        mx,
        my
    ):
        
        if self.left_button_rect.collidepoint(
            mx,
            my
        ):
            self.move_left()

            return True
        
        if self.right_button_rect.collidepoint(
            mx,
            my
        ):
            self.move_right()

            return True

        return None