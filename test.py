import requests
import time
import random

url = "http://localhost:8080/upload/moisture"
sensor_id = "moisture_01"

while True:
    payload = {
        "sensor_id": sensor_id,
        "data": {
            "soil_moisture": random.randint(30, 90)
        }
    }
    try:
        response = requests.post(url, json=payload)
        print(f"[Moisture] Status: {response.status_code} | Response: {response.text}")
    except Exception as e:
        print(f"❌ Error sending moisture data: {e}")
    time.sleep(5)
