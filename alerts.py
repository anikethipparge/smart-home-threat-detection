# utils/alerts.py
import requests
import cv2
import os
from datetime import datetime
from config import TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID

def send_telegram_alert(threat, frame):
    try:
        os.makedirs("alerts", exist_ok=True)
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        image_path = f"alerts/{threat['class']}_{timestamp}.jpg"
        
        cv2.imwrite(image_path, frame)

        url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendPhoto"
        
        caption = f"""
🚨 SMART HOME ALERT 🚨

Threat: {threat['class'].upper()}
Confidence: {threat['confidence']:.2f}
Time: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
        """.strip()

        with open(image_path, 'rb') as photo:
            files = {'photo': photo}
            data = {'chat_id': TELEGRAM_CHAT_ID, 'caption': caption}
            
            response = requests.post(url, data=data, files=files, timeout=15)
            
        if response.status_code == 200:
            print(f"✅ Telegram Alert Sent: {threat['class']}")
        else:
            print(f"❌ Telegram Failed: {response.text}")

    except Exception as e:
        print(f"❌ Error sending Telegram alert: {e}")


def log_threat(class_name, zone_name, confidence):
    try:
        os.makedirs("logs", exist_ok=True)
        import csv
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        file_path = "logs/threat_logs.csv"
        file_exists = os.path.isfile(file_path)
        
        with open(file_path, 'a', newline='') as f:
            writer = csv.writer(f)
            if not file_exists:
                writer.writerow(['Timestamp', 'Threat', 'Zone', 'Confidence'])
            writer.writerow([timestamp, class_name, zone_name, round(confidence, 4)])
    except:
        pass