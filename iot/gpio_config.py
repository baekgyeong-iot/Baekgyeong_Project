# gpio_config.py

# =========================
# 센서
# =========================

LIGHT_SENSOR_PIN = 17

TOUCH_SENSOR_PIN = 27

LEFT_BUTTON_PIN = 23

RIGHT_BUTTON_PIN = 24

TILT_SENSOR_PIN = 27





# =========================
# LED 
# =========================

HUNGER_LED_PIN = 5

ENERGY_LED_PIN = 6

FUN_LED_PIN = 13


# =========================
# 스피커
# =========================

SPEAKER_PIN = 18

# ========================= 
# GAME CONFIG 
# ========================= 
WARNING_THRESHOLD = 10 

YELLOW_THRESHOLD = 50 

RED_THRESHOLD = 30 


# 각 행동의 재사용 대기시간
ACTION_COOLDOWN = { 
  "FEED": 5, 
  "PLAY": 5, 
  "SPEAK": 3, 
  "PET": 2
}
