# Baekgyeong Project

라즈베리파이 기반 스마트 다마고치 프로젝트입니다. 백경이의 상태는 `game_logic`이 관리하고, 웹 대시보드, LCD pygame 화면, IoT 센서/LED는 이벤트를 통해 상태를 변경하거나 조회합니다.

## 실행 방법

### Flask 백엔드 실행

```bash
cd ~/Desktop/Baekgyeong_Project
python app.py
```

기본 포트는 `5050`입니다.

### 웹 대시보드 실행

```bash
cd ~/Desktop/Baekgyeong_Project/ui/src
npm run dev
```

브라우저에서 `http://localhost:5173/` 접속.

### LCD pygame 실행

```bash
cd ~/Desktop/Baekgyeong_Project
python ui/lcd/lcd_main.py
```

LCD가 Flask 서버와 같은 상태를 보려면 `app.py`를 먼저 실행해야 합니다.

### MQTT 브릿지 실행

```bash
cd ~/Desktop/Baekgyeong_Project
python mqtt_client.py
```

MQTT 브로커는 기본적으로 `localhost:1883`을 사용합니다.

## 주요 폴더 역할

`game_logic/`  
백경이 상태, 행동 처리, 시간 감소, 진화, 가출, 저장 로직을 담당합니다.

`ui/src/`  
웹 대시보드입니다. Flask API를 호출해서 상태와 로그를 보여줍니다.

`ui/lcd/`  
pygame 기반 LCD 화면입니다. 버튼/게임 화면을 그리고 이벤트를 발생시킵니다.

`iot/`  
센서, LED, 스피커 쪽 예시 코드입니다. 실제 라즈베리파이 연결 시 GPIO/MQTT 처리를 보강해야 합니다.

## Game Logic Event Contract

모든 팀원은 아래 이벤트 이름과 payload 형식을 기준으로 맞춰주세요.

### 밥 먹기 완료

```json
{
  "source": "LCD",
  "event": "FEED_GAME_FINISHED",
  "payload": {
    "hunger_delta": 10,
    "caught_food_ids": [1, 2]
  }
}
```

처리 결과:
- `hunger` 증가
- `feed_count` 증가
- 진화 조건 검사

### 놀이 완료

```json
{
  "source": "LCD",
  "event": "PLAY_GAME_FINISHED",
  "payload": {
    "game_type": "memory",
    "score": 80,
    "fun_delta": 10
  }
}
```

처리 결과:
- `fun` 증가
- `play_count` 증가
- 진화 조건 검사

### 잠 시작

```json
{
  "source": "LCD",
  "event": "SLEEP_STARTED",
  "payload": {}
}
```

처리 결과:
- `is_sleeping = true`
- mood가 `SLEEPING`으로 변경

### 잠 회복 tick

```json
{
  "source": "SYSTEM",
  "event": "SLEEP_TICK",
  "payload": {
    "energy_delta": 1
  }
}
```

처리 결과:
- 잠자는 중일 때만 `energy` 증가

### 잠 종료

```json
{
  "source": "LCD",
  "event": "SLEEP_ENDED",
  "payload": {
    "full_energy_delta": 10
  }
}
```

처리 결과:
- `is_sleeping = false`
- `energy` 증가
- `sleep_count` 증가
- 진화 조건 검사

### 조도 센서 변경

```json
{
  "source": "LIGHT_SENSOR",
  "event": "LIGHT_CHANGED",
  "payload": {
    "light_value": 80,
    "is_dark": true
  }
}
```

처리 결과:
- 어두워지면 잠 시작
- 자는 중 밝아지면 잠 종료

### 쓰다듬기

```json
{
  "source": "TOUCH_SENSOR",
  "event": "STROKE_ATTEMPT",
  "payload": {
    "date": "2026-06-04"
  }
}
```

처리 결과:
- 하루 1회 성공
- 성공 시 `favorability` 증가
- 같은 날짜에 다시 시도하면 실패 로그 반환

### 시간 흐름

```json
{
  "source": "SYSTEM",
  "event": "TIME_TICK",
  "payload": {
    "hunger_delta": -1,
    "fun_delta": -1,
    "energy_delta": -1
  }
}
```

처리 결과:
- `hunger`, `fun`, `energy` 감소
- 자는 중에는 `energy` 감소 없음
- 가출 조건 검사

### 서버 재시작 시 오프라인 시간 반영

```json
{
  "source": "SYSTEM",
  "event": "APPLY_OFFLINE_PROGRESS",
  "payload": {
    "tick_interval_seconds": 60
  }
}
```

처리 결과:
- 서버가 꺼져 있던 동안의 시간만큼 상태 감소
- 긴 시간 방치 시 가출 처리 가능

### 진화 검사

```json
{
  "source": "SYSTEM",
  "event": "EVO_CHECK",
  "payload": {
    "trigger": "manual",
    "date": "2026-06-04"
  }
}
```

처리 결과:
- 조건 충족 시 `growth_stage` 변경

### 가출 검사

```json
{
  "source": "SYSTEM",
  "event": "RUNAWAY_CHECK",
  "payload": {
    "date": "2026-06-04"
  }
}
```

처리 결과:
- 위험 상태가 유지되면 `is_runaway = true`

### 새 백경이 시작

```json
{
  "source": "LCD",
  "event": "NEW_BAEKGYEONG_REQUESTED",
  "payload": {
    "birth_date": "2026-06-04"
  }
}
```

처리 결과:
- 모든 상태 초기화

## MQTT Topics

IoT/LCD가 MQTT를 사용할 때는 아래 topic을 기준으로 맞춥니다.

| 역할 | Topic | 대표 이벤트 |
| --- | --- | --- |
| 조도 센서 | `baekgyeong/sensor/light` | `LIGHT_CHANGED` |
| 자이로/흔들기 센서 | `baekgyeong/sensor/gyro` | `DEVICE_SHAKEN` |
| 기울기 센서 | `baekgyeong/sensor/tilt` | `DEVICE_SHAKEN` |
| LCD 이벤트 | `baekgyeong/event/lcd` | `FEED_GAME_FINISHED`, `PLAY_GAME_FINISHED` |
| 터치/쓰다듬기 | `baekgyeong/action/pet` | `PET_DETECTED` |
| 대화 버튼 | `baekgyeong/action/text` | `TEXT_BUTTON_CLICKED` |
| 상태 업데이트 수신 | `baekgyeong/state/update` | `STATE_UPDATED` |
| LED 제어 수신 | `baekgyeong/led/control` | `LED_UPDATE` |

MQTT payload는 JSON 문자열로 보냅니다.

```python
import json
import paho.mqtt.client as mqtt

client = mqtt.Client()
client.connect("localhost", 1883)

client.publish(
    "baekgyeong/event/lcd",
    json.dumps({
        "source": "LCD",
        "event": "FEED_GAME_FINISHED",
        "payload": {
            "hunger_delta": 10,
            "caught_food_ids": [1, 2]
        }
    }, ensure_ascii=False)
)
```

## Flask API

웹 대시보드는 Flask API를 사용합니다.

| Method | URL | 설명 |
| --- | --- | --- |
| GET | `/api/state` | 현재 백경이 상태 조회 |
| GET | `/api/logs` | 최근 이벤트 로그 조회 |
| GET | `/api/led` | 현재 LED 색 상태 조회 |
| POST | `/api/event` | game_logic 이벤트 전달 |
| POST | `/api/reset` | 새 백경이로 초기화 |

## 담당자별 기준

### game_logic 담당

- 이벤트 이름과 payload 형식을 유지합니다.
- 상태 변경 규칙, 진화, 가출, 저장 로직을 관리합니다.
- UI/IoT에서 잘못된 payload가 와도 최대한 안전하게 처리되도록 점검합니다.

### UI/LCD 담당

- 화면과 게임 진행을 담당합니다.
- 수치를 직접 계산하지 말고 게임 결과 이벤트만 보냅니다.
- 예: 먹기 게임 종료 시 `FEED_GAME_FINISHED`, 놀이 종료 시 `PLAY_GAME_FINISHED`.

### IoT 담당

- 센서 값을 읽어서 정해진 MQTT 이벤트로 publish합니다.
- LED는 `baekgyeong/led/control`을 subscribe해서 출력합니다.
- 실제 GPIO 핀 번호와 센서 기준값은 라즈베리파이에서 최종 확인합니다.

## 테스트 시나리오

1. `POST /api/reset` 또는 `NEW_BAEKGYEONG_REQUESTED`로 초기화
2. `FEED_GAME_FINISHED` 전송 후 `hunger`, `feed_count` 증가 확인
3. `PLAY_GAME_FINISHED` 전송 후 `fun`, `play_count` 증가 확인
4. `SLEEP_STARTED` 전송 후 `is_sleeping = true` 확인
5. `SLEEP_ENDED` 전송 후 `energy`, `sleep_count` 증가 확인
6. `TIME_TICK` 전송 후 수치 감소 확인
7. `STROKE_ATTEMPT` 전송 후 호감도 증가 또는 중복 실패 확인
8. 진화 조건 충족 후 `growth_stage` 변경 확인
9. 가출 조건 충족 후 `is_runaway = true` 확인
