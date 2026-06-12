#scene_manager.py 
import pygame
import random

from scenes.main_scene import MainScene

from scenes.feed_confirm_scene import FeedConfirmScene
from scenes.feed_game_scene import FeedGameScene
from scenes.feed_result_scene import FeedResultScene

from scenes.play_game_select_scene import PlayGameSelectScene
from scenes.blue_red_flag_scene import BlueRedFlagScene
from scenes.memory_game_scene import MemoryGameScene
from scenes.gyro_game_scene import GyroGameScene
from scenes.play_result_scene import PlayResultScene
from scenes.popup_scene import PopupScene
from scenes.sleep_scene import SleepScene

from scenes.popup_scene import PopupScene
from scenes.runaway_scene import RunawayScene
from scenes.gift_scene import GiftScene

message_table = {
    "BABY": {
        "0_20": [
            "어색해...",
            "놀아줘..."
        ],
        "21_40": [
            "오늘은 기분이 좋아!",
            "같이 있어줘서 고마워!"
        ],
        "41_60": [
            "오늘도 즐거워!",
            "너랑 노는 게 좋아!"
        ],
        "61_80": [
            "항상 고마워!",
            "너를 보면 힘이 나!"
        ],
        "81_100": [
            "제일 좋아해!",
            "항상 함께하고 싶어!"
        ]

    },

    "CHILD": {
        "0_20": [
            "아직 조금 어색해.",
            "무슨 말을 해야 할까?"
        ],
        "21_40": [
            "오늘도 왔네!",
            "반가워!"
        ],
        "41_60": [
            "같이 놀자!",
            "오늘은 뭐 할까?"
        ],
        "61_80": [
            "너랑 있으면 재밌어!",
            "기다리고 있었어!"
        ],
        "81_100": [
            "네가 최고야!",
            "정말 좋아해!"
        ]
    },

    "ADULT": {
        "0_20": [
            "아직은 너가 어려워.",
            "천천히 친해지자."
        ],
        "21_40": [
            "오늘도 와줘서 고마워.",
            "네가 오면 기분이 좋아"
        ],
        "41_60": [
            "오늘 하루는 어땠어?",
            "같이 이야기하자."
        ],
        "61_80": [
            "널 보면 힘이 나.",
            "오늘도 반가워"
        ],
        "81_100": [
            "항상 함께해줘서 고마워.",
            "너는 정말 소중한 존재야."
        ]
    }
}

gift_table = {
    1: "작은 조개껍데기",
    2: "반짝이는 돌",
    3: "바다 유리"
}

class SceneManager:

    def __init__(
        self,
        screen,
        state,
        sprites,
        icons,
        food_sprites,
        font_sm,
        font_md,
        font_lg
    ):

        self.screen = screen

        self.state = state

        self.sprites = sprites
        self.icons = icons
        self.food_sprites = food_sprites

        self.font_sm = font_sm
        self.font_md = font_md
        self.font_lg = font_lg

        self.feed_result = None
        self.play_result = None

        self.mqtt_client = None

        self.current_scene = MainScene(
            screen,
            state,
            sprites,
            icons,
            font_sm,
            font_md,
            font_lg
        )

    # -------------------------
    # draw
    # -------------------------

    def draw(self):

        if not self.current_scene:
            return

        self.current_scene.draw()

        # -------------------------
        # update
        # -------------------------

        if hasattr(
            self.current_scene,
            "update"
        ):
            self.current_scene.update()

        # -------------------------
        # FeedGame 종료 검사
        # -------------------------

        if isinstance(
            self.current_scene,
            FeedGameScene
        ):

            if self.current_scene.is_finished():

                result = (
                    self.current_scene
                    .get_result()
                )

                self.feed_result = result

                raw_hunger_delta = (
                    result["hunger_delta"]
                )

                hunger_delta = result["hunger_delta"]

                self.state["hunger"] = min(
                    100,
                    self.state["hunger"]
                    + hunger_delta
                )

                # MQTT 발행

                if self.mqtt_client:

                    self.mqtt_client.publish_feed_finished(
                        hunger_delta,
                        result[
                            "caught_food_ids"
                        ]
                    )

                print(
                    "[FEED_GAME_FINISHED]"
                )

                print(result)

                self.change_scene(
                    "FEED_GAME_FINISHED"
                )
        # -------------------------
        # Play Games
        # -------------------------

        elif isinstance(
            self.current_scene,
            (
                BlueRedFlagScene,
                MemoryGameScene,
                GyroGameScene
            )
        ):

            if self.current_scene.is_finished():

                result = (
                    self.current_scene
                    .get_result()
                )

                self.change_scene(
                    "PLAY_GAME_FINISHED",
                    result
            ) 

        # -------------------------
        # Gifts
        # ------------------------- 

        elif isinstance(
            self.current_scene,
            GiftScene
        ):

            if self.current_scene.is_finished():

                self.current_scene = PopupScene(
                    self.screen,
                    "선물을 받았습니다!\n"
                    "받은 선물은\n"
                    "대시보드에서 확인할 수 있습니다.",
                    self.font_sm,
                    self.font_md,
                    self.font_lg
                )    

    # -------------------------
    # 키보드 입력/ 디버깅용
    # -------------------------

    def handle_key(
        self,
        key
    ):

        if not self.current_scene:
            return

        if isinstance(
            self.current_scene,
            FeedGameScene
        ):

            if key == pygame.K_LEFT:

                self.current_scene.move_left()

            elif key == pygame.K_RIGHT:

                self.current_scene.move_right()

        elif isinstance(
            self.current_scene,
            BlueRedFlagScene
        ):

            if key == pygame.K_LEFT:

                self.current_scene.handle_button(
                    "LEFT"
                )

            elif key == pygame.K_RIGHT:

                self.current_scene.handle_button(
                    "RIGHT"
                )            

    # -------------------------
    # click
    # -------------------------

    def handle_click(
        self,
        mx,
        my
    ):

        if not hasattr(
            self.current_scene,
            "handle_click"
        ):
            return None

        click_result = (
            self.current_scene.handle_click(
                mx,
                my
            )
        )

        payload = None

        if isinstance(click_result, dict):

            event_name = click_result.get(
                "event"
            )

            payload = click_result.get(
                "payload",
                {}
            )

        else:

            event_name = click_result

        if event_name:

            self.publish_event(
                event_name,
                payload
            )

            self.change_scene(
                event_name,
                payload
            )

        return event_name
    
    # =====================
    # 호감도 구간 계산
    # =====================

    def get_favorability_range(self, favorability):

        if favorability <= 20:
            return "0_20"
        
        elif favorability <= 40:
            return "21_40"
        
        elif favorability <= 60:
            return "41_60"
        
        elif favorability <= 80:
            return "61_80"
        
        return "81_100"
    
    # -------------------------
    # MQTT Publish
    # -------------------------

    def publish_event(
            self,
            event_name,
            payload=None
    ):
        if not self.mqtt_client:
            return
        
        payload = payload or {}

        try:

            if event_name == "FEED_BUTTON_CLICKED":
                
                self.mqtt_client.publish_feed_button_clicked()
            
            elif event_name == "FEED_CONFIRMED":

                self.mqtt_client.publish_feed_confirmed()
            
            elif event_name == "FEED_CANCELLED":

                self.mqtt_client.publish_feed_cancelled()

            elif event_name == "SLEEP_BUTTON_CLICKED":

                self.mqtt_client.publish_sleep_button_clicked()

            elif event_name == "PLAY_BUTTON_CLICKED":

                self.mqtt_client.publish_play_button_clicked()

            elif event_name == "TEXT_BUTTON_CLICKED":

                self.mqtt_client.publish_text_button_clicked()

            elif event_name == "STROKE_ATTEMPT":

                from datetime import datetime

                self.mqtt_client.publish_stroke_attempt(
                    datetime.now().strftime(
                        "%Y-%m-%d"
                    )
                )
            
            elif event_name == ("NEW_BAEKGYEONG_REQUESTED"):
                self.mqtt_client.publish_new_baekgyeong()
            
        except Exception as e:

            print(
                "[MQTT PUBLISH ERROR]",
                e
            )
    
    # ------------------------------------------------
    # MQTT Event Receiver 진입점
    # ------------------------------------------------

    def handle_system_event(
        self,
        event_name,
        payload=None
    ):

        payload = payload or {}

        print(
            f"[SYSTEM EVENT] {event_name}"
        )

        if (
            self.current_scene
            and
            hasattr(
                self.current_scene,
                "handle_system_event"
            )
        ):
            self.current_scene.handle_system_event(
                event_name,
                payload
            )

        self.change_scene(
            event_name,
            payload
        )
            

    # -------------------------
    # Scene Change
    # -------------------------

    def change_scene(
        self,
        event_name,
        payload=None
    ):
        
        payload = payload or {}  

        # =====================
        # 밥주기
        # =====================

        if event_name == "FEED_BUTTON_CLICKED":

            print(
                "FeedConfirmScene 진입"
            )

            self.current_scene = (
                FeedConfirmScene(
                    self.screen,
                    self.state,
                    self.sprites,
                    self.icons,
                    self.font_sm,
                    self.font_md,
                    self.font_lg
                )
            )

        elif event_name == "FEED_CONFIRMED":

            print(
                "FeedGameScene 시작"
            )

            self.current_scene = (
                FeedGameScene(
                    self.screen,
                    self.state,
                    self.sprites,
                    self.food_sprites,
                    self.font_sm,
                    self.font_md,
                    self.font_lg
                )
            )

        elif event_name == "FEED_CANCELLED":

            self.go_home()

        elif event_name == "FEED_GAME_FINISHED":

            print("Feed Game 종료")

            self.current_scene = FeedResultScene(
                self.screen,
                self.feed_result,
                self.font_sm,
                self.font_md,
                self.font_lg
            )
        
        elif event_name == "FEED_RESULT_CONFIRMED":

            self.go_home()

        # =====================
        # 잠자기
        # =====================

        elif event_name == "SLEEP_BUTTON_CLICKED":

            print("Sleep Scene 진입")

            self.current_scene = PopupScene(
                self.screen,
                "조도 센서를 확인하는 중...",
                self.font_sm,
                self.font_md,
                self.font_lg
            )

        elif event_name == "SLEEP_WAITING_DARK":

            print("어두워질 때까지 대기")

            self.current_scene = PopupScene(
                self.screen,
                "조도 센서를 가려주세요",
                self.font_sm,
                self.font_md,
                self.font_lg
            )

        elif event_name == "SLEEP_STARTED":

            self.state["is_sleeping"] = True

            self.current_scene = (
                SleepScene(
                    self.screen,
                    self.state,
                    self.sprites,
                    self.font_sm,
                    self.font_md,
                    self.font_lg
                )
            )
        elif event_name == "SLEEP_TICK":

            energy_delta = payload.get(
                "energy_delta",
                0
            )

            self.state["energy"] = min(
                100,
                self.state["energy"]
                + energy_delta
            )

        elif event_name == "SLEEP_ENDED":

            self.state["is_sleeping"] = False

            self.state["energy"] = (
                payload.get(
                    "current_energy",
                    self.state["energy"]
                )
            )

            self.go_home()

        # =====================
        # 놀이
        # =====================

        elif event_name == "PLAY_BUTTON_CLICKED":

            self.current_scene = (
                PlayGameSelectScene(
                    self.screen,
                    self.font_sm,
                    self.font_md,
                    self.font_lg
                )
            )

        elif event_name == "PLAY_GAME_SELECTED":

            game_type = payload.get("game_type")

            if self.mqtt_client:

                self.mqtt_client.publish_play_selected(
                    game_type
                )

            if game_type == "blue_red_flag":
                
                self.current_scene = (
                    BlueRedFlagScene(
                        self.screen,
                        self.state,
                        self.sprites,
                        self.mqtt_client,
                        self.font_sm,
                        self.font_md,
                        self.font_lg
                    )
                )
            
            elif game_type == "memory":

                self.current_scene = (
                    MemoryGameScene(
                        self.screen,
                        self.state,
                        self.sprites,
                        self.font_sm,
                        self.font_md,
                        self.font_lg
                    )
                )
            
            elif game_type == "red_light_green_light":

                self.current_scene = (
                    GyroGameScene(
                        self.screen,
                        self.state,
                        self.mqtt_client,
                        self.font_sm,
                        self.font_md,
                        self.font_lg
                    )
                )

        elif event_name == "PLAY_GAME_FINISHED":

            fun_delta = payload.get(
                "fun_delta",
                0
            )

            self.state["fun"] = min(
                100,
                self.state.get(
                    "fun",
                    0
                ) + fun_delta
            )

            self.play_result = payload

            if self.mqtt_client:

                self.mqtt_client.publish_play_finished(
                    payload.get(
                        "game_type"
                    ),
                    payload.get(
                        "score",
                        0
                    ),
                    fun_delta
                )

            self.current_scene = (
                PlayResultScene(
                    self.screen,
                    payload,
                    self.font_sm,
                    self.font_md,
                    self.font_lg
                )
            )

        elif event_name == "PLAY_RESULT_CLOSE":
            
            self.go_home()  

        # =====================
        # 대화
        # =====================

        elif event_name == "TEXT_BUTTON_CLICKED":

            print("대화 화면")

            growth_stage = self.state.get(
                "growth_stage",
                "BABY"
            )

            favorability = self.state.get(
                "favorability",
                0
            )

            favorability_range = (
                self.get_favorability_range(
                    favorability
                )
            )

            message = (
                message_table
                .get(growth_stage, {})
                .get(favorability_range, [])
            )

            if not message:
                selected_message = "..."
            else:
                selected_message = random.choice(message)
            
            self.state["current_message"] = selected_message

            if self.mqtt_client:
                import time
                self.mqtt_client.message_lock_until = time.time() + 5

            self.go_home()

        elif event_name == "POPUP_CLOSE":

            self.go_home()

        # =====================
        # 쓰다듬기
        # =====================

        elif event_name == "STROKE_ATTEMPT":

            print(
                "쓰다듬기 시도"
            )

        elif event_name == "STROKE_RESULT":

            success = payload.get(
                "success",
                False
            )

            if success:

                self.state["favorability"] = (
                    payload.get(
                        "current_favorability",
                        self.state["favorability"]
                    )
                )

                self.state["current_message"] = (
                    f"♥ 호감도 +{payload.get('favorability_delta',0)}"
                )

                if isinstance(
                    self.current_scene,
                    MainScene
                ):
                    self.current_scene.play_stroke_success_animation()
            
            else:

                remain = payload.get(
                    "cooldown_remaining",
                    0
                )

                self.current_scene = PopupScene(
                    self.screen,
                    f"지금은 쓰다듬을 수 없어요.\n"
                    f"({remain}시간 남음)",
                    self.font_sm,
                    self.font_md,
                    self.font_lg
                )

        # =====================
        # 선물
        # =====================

        elif event_name == "GIFT_DAILY_CHECK":

            print(
                "선물 검사"
            )

        elif event_name == "GIFT_EVENT_TRIGGERED":

            gift_id = payload.get("gift_id")

            gift_name = gift_table.get(
                gift_id,
                "알 수 없는 선물"
            )

            self.current_scene = GiftScene(
                self.screen,
                self.state,
                self.sprites,
                self.font_md,
                self.font_lg,
                gift_name
            )

            print(
                "선물 획득"
            )

        # =====================
        # 진화
        # =====================

        elif event_name == "EVO_CHECK":

            print(
                "진화 조건 검사"
            )

        elif event_name == "EVO_EVENT_TRIGGERED":

            from_stage = payload.get(
                "from_stage",
                "BABY"
            )

            to_stage = payload.get(
                "to_stage",
                "CHILD"
            )

            print(f"[EVOLUTION] {from_stage} -> {to_stage}")

            # 상태 업데이트
            self.state["growth_stage"] = to_stage

            # 새 성장단계 스프라이트
            evolution_sprite = None

            if (
                to_stage in self.sprites
                and
                len(
                    self.sprites[to_stage]["BASIC"]
                ) > 0
            ):
                evolution_sprite = self.sprites[to_stage]["BASIC"][0]

            stage_name = {
                "BABY": "아기",
                "CHILD": "청소년",
                "ADULT": "성인"
            }

            self.current_scene = PopupScene(
                self.screen,
                f"{stage_name.get(to_stage,to_stage)}단계가 되었어요",
                self.font_sm,
                self.font_md,
                self.font_lg,
                popup_type = "evolution",
                evolution_sprite= evolution_sprite
            )

        elif event_name == "EVOLUTION_CONFIRMED":

            print("[EVOLUTION COMPLETE]")

            self.go_home()

        # =====================
        # 가출
        # =====================

        elif event_name == "RUNAWAY_CHECK":

            print(
                "가출 조건 검사"
            )

        elif event_name == "RUNAWAY_EVENT_TRIGGERED":

            self.state["is_runaway"] = True

            self.state["runaway_reason"] = payload.get(
                "reason",
                ""
            )

            self.current_scene = RunawayScene(
                self.screen,
                self.sprites,
                self.state,
                self.font_sm,
                self.font_md,
                self.font_lg
            )

            print(
                "가출 발생"
            )

        elif event_name == "NEW_BAEKGYEONG_REQUESTED":

            print("[NEW BAEKGYEONG REQUEST SENT]")

            self.go_home()

    # -------------------------
    # Home
    # -------------------------

    def go_home(self):

        self.current_scene = MainScene(
            self.screen,
            self.state,
            self.sprites,
            self.icons,
            self.font_sm,
            self.font_md,
            self.font_lg
        )
