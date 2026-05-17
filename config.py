# =============================================
# config.py
# =============================================

# Model Settings
MODEL_PATH = "yolov8n.pt"
CONFIDENCE_THRESHOLD = 0.5
IOU_THRESHOLD = 0.45

# Threat Classes
THREAT_CLASSES = {
    'person', 'knife', 'gun', 'pistol', 
    'fire', 'smoke'
}

# Camera Settings
CAMERA_URL = 0
FRAME_WIDTH = 640
FRAME_HEIGHT = 480

# Alert Settings
ALERT_COOLDOWN_SECONDS = 30

# ================= TELEGRAM =================
TELEGRAM_BOT_TOKEN = "8861200195:AAHN3utogJYsjSApadCRU46qpDEte-YvaU4"
TELEGRAM_CHAT_ID = "7020841062"

# Monitoring Zones
ENTRY_ZONES = {
    "front_door": [50, 150, 300, 450],
    "window": [350, 100, 550, 300],
    "back_area": [400, 350, 620, 480]
}