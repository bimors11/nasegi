import requests
import time
import random

url = "http://localhost:8080/upload/humidity"
sensor_id = "humidity_01"

while True:
    payload = {
        "sensor_id": sensor_id,
        "data": {
            "humidity": random.randint(40, 100)
        }
    }
    try:
        response = requests.post(url, json=payload)
        print(f"[Humidity] Status: {response.status_code} | Response: {response.text}")
    except Exception as e:
        print(f"❌ Error sending humidity data: {e}")
    time.sleep(5)
