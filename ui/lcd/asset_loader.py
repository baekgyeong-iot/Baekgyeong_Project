# ui/lcd/asset_loader.py

import pygame
import os


# -----------------------------
# 프로젝트 루트
# baekgyeong_iot
# -----------------------------

BASE_DIR = os.path.dirname(
    os.path.dirname(
        os.path.dirname(
            os.path.abspath(__file__)
        )
    )
)

# -----------------------------
# 경로
# -----------------------------

SPRITE_DIR = os.path.join(
    BASE_DIR,
    "assets",
    "sprites"
)

ICON_DIR = os.path.join(
    SPRITE_DIR,
    "ui"
)

FOOD_DIR = os.path.join(
    SPRITE_DIR,
    "foods"
)


# -----------------------------
# 폰트
# -----------------------------

def load_fonts():

    try:

        font_sm = pygame.font.SysFont(
            "malgungothic",
            13,
            bold=True
        )

        font_md = pygame.font.SysFont(
            "malgungothic",
            15,
            bold=True
        )

        font_lg = pygame.font.SysFont(
            "malgungothic",
            18,
            bold=True
        )

    except Exception:

        font_sm = pygame.font.Font(
            None,
            16
        )

        font_md = pygame.font.Font(
            None,
            20
        )

        font_lg = pygame.font.Font(
            None,
            24
        )

    return (
        font_sm,
        font_md,
        font_lg
    )


# -----------------------------
# 공용 이미지 로더
# -----------------------------

def load_image(path, size=None):

    if not os.path.exists(path):

        print(f"[FAIL] {path}")
        return None

    image = pygame.image.load(
        path
    ).convert_alpha()

    if size:

        image = pygame.transform.scale(
            image,
            size
        )

    print(
        f"[OK] {os.path.basename(path)}"
    )

    return image


# -----------------------------
# 아이콘
# -----------------------------

def load_icons():

    print("\n=== ICON LOAD START ===")
    print(ICON_DIR)

    icons = {}

    icon_files = {
        "hunger": "icon_hunger.png",
        "energy": "icon_sleep.png",
        "fun": "icon_game.png",
        "favorability": "icon_favorability.png",
        "talk": "icon_talk.png"
    }

    for key, filename in icon_files.items():

        path = os.path.join(
            ICON_DIR,
            filename
        )

        icons[key] = load_image(
            path,
            (40, 40)
        )

    print("=== ICON LOAD END ===\n")

    return icons


# -----------------------------
# 음식 스프라이트
# -----------------------------

def load_food_sprites():

    print("\n=== FOOD LOAD START ===")
    print(FOOD_DIR)

    foods = {}

    food_files = {
        "shrimp": "shrimp.png",
        "fishcake": "fishcake.png",
        "fish": "fish.png"
    }

    for key, filename in food_files.items():

        path = os.path.join(
            FOOD_DIR,
            filename
        )

        foods[key] = load_image(
            path,
            (48, 48)
        )

    print("=== FOOD LOAD END ===\n")

    return foods


# -----------------------------
# 백경이 스프라이트
# -----------------------------

def load_sprites():

    print("\n=== SPRITE LOAD START ===")
    print(SPRITE_DIR)

    sprites = {}

    stages = {
        "BABY": "baby",
        "CHILD": "child",
        "ADULT": "adult"
    }

    for stage, folder in stages.items():

        print(f"\n[{stage}]")

        folder_path = os.path.join(
            SPRITE_DIR,
            folder
        )

        sprites[stage] = {

            # 메인화면
            "BASIC": [],
            # 먹기 게임
            "FEED":[],
            "LEFT":[],
            "RIGHT":[],
            # 청기백기
            "BLUE_RED_LEFT":[],
            "BLUE_RED_RIGHT":[],

            "SLEEP": None,
            "SMILE": None,
            "SHY": None,
            "PRESENT": None,

            #가출
            "RUNAWAY": None
        }

        # -----------------
        # 메인화면 기본
        # -----------------

        for i in [1, 2]:

            sprites[stage]["BASIC"].append(

                load_image(
                    os.path.join(
                        folder_path,
                        f"{folder}_baekgyeong{i}.png"
                    ),
                    (110, 110)
                )
            )

        # -----------------
        # 감정
        # -----------------

        sprites[stage]["SLEEP"] = load_image(
            os.path.join(
                folder_path,
                f"{folder}_baekgyeong_sleep.png"
            ),
            (110, 110)
        )

        sprites[stage]["SMILE"] = load_image(
            os.path.join(
                folder_path,
                f"{folder}_baekgyeong_smile.png"
            ),
            (110, 110)
        )

        sprites[stage]["SHY"] = load_image(
            os.path.join(
                folder_path,
                f"{folder}_baekgyeong_shy.png"
            ),
            (110, 110)
        )

        sprites[stage]["PRESENT"] = load_image(
            os.path.join(
                folder_path,
                f"{folder}_baekgyeong_present.png"
            ),
            (110, 110)
        )

        # -----------------
        # 가출 스프라이트
        # -----------------

        sprites[stage]["RUNAWAY"] = load_image(
            os.path.join(
                folder_path,
                f"{folder}_runaway.png"
            ),
            (110, 110)
        )

        # ==================================
        # 먹기게임 전용
        # ==================================

        # 입벌리고 위 보기
        for i in [1, 2]:

            sprites[stage]["FEED"].append(

                load_image(
                    os.path.join(
                        folder_path,
                        f"{folder}_feed{i}.png"
                    ),
                    (110, 110)
                )
            )

        # 왼쪽 이동
        for i in [1, 2]:

            sprites[stage]["LEFT"].append(

                load_image(
                    os.path.join(
                        folder_path,
                        f"{folder}_left{i}.png"
                    ),
                    (110, 110)
                )
            )

        # 오른쪽 이동
        for i in [1, 2]:

            sprites[stage]["RIGHT"].append(

                load_image(
                    os.path.join(
                        folder_path,
                        f"{folder}_right{i}.png"
                    ),
                    (110, 110)
                )
            )
        
        # -----------------
        # 청기백기 전용
        # -----------------

        sprites[stage]["BLUE_RED_LEFT"] = load_image(
            os.path.join(
                folder_path,
                f"{folder}_blue_red_left.png"
            ),
            (110, 110)
        )

        sprites[stage]["BLUE_RED_RIGHT"] = load_image(
            os.path.join(
                folder_path,
                f"{folder}_blue_red_right.png"
            ),
            (110, 110)
        )

    print("\n=== SPRITE LOAD END ===\n")

    return sprites