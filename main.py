# =====================================================
# main.py - Smart Home Threat Detection (Fixed Imports)
# =====================================================

import sys
import os

# Add current directory to Python path (Fix for ModuleNotFoundError)
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from ultralytics import YOLO
import cv2
import time
import threading

# Now import config and utils
from config import *
from utils.alerts import send_telegram_alert, log_threat
from utils.zones import is_in_zone, draw_zones

# ====================== INITIALIZATION ======================
print("🚀 Starting Smart Home Threat Detection...")

os.makedirs("model", exist_ok=True)
os.makedirs("alerts", exist_ok=True)
os.makedirs("logs", exist_ok=True)

# Use default model if custom model not found
if not os.path.exists(MODEL_PATH):
    print(f"⚠️ Model {MODEL_PATH} not found. Using yolov8n.pt")
    MODEL_PATH = "yolov8n.pt"

print(f"✅ Loading Model: {MODEL_PATH}")
model = YOLO(MODEL_PATH)
print("✅ Model loaded successfully!\n")

# ====================== CAMERA ======================
cap = cv2.VideoCapture(CAMERA_URL)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, FRAME_WIDTH)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, FRAME_HEIGHT)

if not cap.isOpened():
    print("❌ Cannot open camera! Check CAMERA_URL in config.py")
    exit()

print("🎥 Camera started")
print("Press 'q' to quit\n")

alert_cooldown = {}

# ====================== MAIN LOOP ======================
while True:
    ret, frame = cap.read()
    if not ret:
        break

    original_frame = frame.copy()

    # YOLO Detection
    results = model(frame, conf=CONFIDENCE_THRESHOLD, iou=IOU_THRESHOLD, verbose=False)

    threats_in_frame = []

    for result in results:
        for box in result.boxes:
            x1, y1, x2, y2 = map(int, box.xyxy[0])
            conf = float(box.conf[0])
            cls_id = int(box.cls[0])
            class_name = result.names[cls_id]

            if class_name in THREAT_CLASSES and conf >= CONFIDENCE_THRESHOLD:
                cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 0, 255), 3)
                label = f"{class_name} {conf:.2f}"
                cv2.putText(frame, label, (x1, y1-10),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 2)

                threat = {"class": class_name, "confidence": conf, "bbox": (x1,y1,x2,y2)}
                threats_in_frame.append(threat)

                for zone_name, zone_coords in ENTRY_ZONES.items():
                    if is_in_zone((x1, y1, x2, y2), zone_coords):
                        log_threat(class_name, zone_name, conf)

    draw_zones(frame, ENTRY_ZONES)

    # Alert
    current_time = time.time()
    if threats_in_frame:
        for threat in threats_in_frame:
            key = threat["class"]
            if key not in alert_cooldown or current_time - alert_cooldown[key] > ALERT_COOLDOWN_SECONDS:
                print(f"🚨 ALERT [{key.upper()}] detected | Confidence: {threat['confidence']:.2f}")

                threading.Thread(
                    target=send_telegram_alert,
                    args=(threat, original_frame),
                    daemon=True
                ).start()

                alert_cooldown[key] = current_time

    cv2.imshow("Smart Home Threat Detection - YOLOv8", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
print("🛑 System Stopped")