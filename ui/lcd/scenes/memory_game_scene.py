import pygame
import random

SCREEN_WIDTH = 480
SCREEN_HEIGHT = 320

COLOR_BG = (73,116,181)

COLOR_WHITE = (255,255,255)
COLOR_BLACK = (0,0,0)

COLOR_BLUE = (100,100,255)
COLOR_RED = (255,100,100)

MAX_ROUND = 5


class MemoryGameScene:

    def __init__(
        self,
        screen,
        state,
        sprites,
        font_sm,
        font_md,
        font_lg
    ):

        self.screen = screen
        self.state = state
        self.sprites = sprites

        self.font_sm = font_sm
        self.font_md = font_md
        self.font_lg = font_lg

        self.finished = False

        self.score = 0

        self.round = 1

        self.sequence = []
        self.user_inputs = []

        self.showing_sequence = True

        self.sequence_index = 0

        self.last_flash = pygame.time.get_ticks()

        self.flash_interval = 800

        self.generate_round()

    def handle_click(self, mx, my):
        return None

    # -------------------------
    # Round 생성
    # -------------------------

    def generate_round(self):

        self.sequence = [

            random.choice(
                ["LEFT","RIGHT"]
            )

            for _ in range(self.round + 2)
        ]

        self.user_inputs = []

        self.sequence_index = 0

        self.showing_sequence = True

        self.last_flash = pygame.time.get_ticks()

    # -------------------------
    # Draw
    # -------------------------

    def draw(self):

        self.screen.fill(
            COLOR_BG
        )

        self.draw_header()

        self.draw_led()

        self.draw_character()

        self.draw_info()

    # -------------------------
    # Header
    # -------------------------

    def draw_header(self):

        title = self.font_md.render(
            f"암기게임 ROUND {self.round}",
            True,
            COLOR_WHITE
        )

        self.screen.blit(
            title,
            (20,20)
        )

        score = self.font_md.render(
            f"점수 {self.score}",
            True,
            COLOR_WHITE
        )

        self.screen.blit(
            score,
            (340,20)
        )

    # -------------------------
    # LED 표시
    # -------------------------

    def draw_led(self):

        left_color = COLOR_WHITE
        right_color = COLOR_WHITE

        if self.showing_sequence:

            now = pygame.time.get_ticks()

            if (
                now - self.last_flash
                <
                400
            ):

                if (
                    self.sequence_index
                    <
                    len(self.sequence)
                ):

                    current = (
                        self.sequence[
                            self.sequence_index
                        ]
                    )

                    if current == "LEFT":

                        left_color = COLOR_BLUE

                    else:

                        right_color = COLOR_RED

        pygame.draw.circle(
            self.screen,
            left_color,
            (140,120),
            35
        )

        pygame.draw.circle(
            self.screen,
            right_color,
            (340,120),
            35
        )

    # -------------------------
    # 캐릭터
    # -------------------------

    def draw_character(self):

        stage = self.state.get(
            "growth_stage",
            "BABY"
        )

        basic = (
            self.sprites
            .get(stage,{})
            .get("BASIC",[])
        )

        if not basic:
            return

        frame = (

            pygame.time.get_ticks()
            // 500

        ) % len(basic)

        sprite = basic[frame]

        self.screen.blit(
            sprite,
            (185,160)
        )

    # -------------------------
    # 설명
    # -------------------------

    def draw_info(self):

        if self.showing_sequence:

            msg = "순서를 기억하세요"

        else:

            msg = "버튼을 입력하세요"

        text = self.font_sm.render(
            msg,
            True,
            COLOR_WHITE
        )

        self.screen.blit(
            text,
            (
                SCREEN_WIDTH//2
                -
                text.get_width()//2,
                280
            )
        )

    # -------------------------
    # Update
    # -------------------------

    def update(self):

        if not self.showing_sequence:
            return

        now = pygame.time.get_ticks()

        if (
            now - self.last_flash
            >
            self.flash_interval
        ):

            self.sequence_index += 1

            self.last_flash = now

            if (
                self.sequence_index
                >=
                len(self.sequence)
            ):

                self.showing_sequence = False

    # -------------------------
    # MQTT 버튼 입력
    # -------------------------

    def handle_button(
        self,
        direction
    ):

        if self.showing_sequence:
            return

        self.user_inputs.append(
            direction
        )

        idx = len(
            self.user_inputs
        ) - 1

        if (

            self.sequence[idx]
            !=
            direction

        ):

            self.finished = True
            return

        self.score += 50

        if (

            len(self.user_inputs)
            ==
            len(self.sequence)

        ):

            self.round += 1

            if self.round > MAX_ROUND:

                self.finished = True

            else:

                self.generate_round()

    # -------------------------
    # 종료 여부
    # -------------------------

    def is_finished(self):

        return self.finished

    # -------------------------
    # 결과 반환
    # -------------------------

    def get_result(self):

        fun_delta = min(
            30,
            self.score // 100
        )

        return {

            "game_type":
                "memory",

            "score":
                self.score,

            "fun_delta":
                fun_delta
        }