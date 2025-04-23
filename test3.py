import requests
import time
import random

url = "http://localhost:8080/upload/temperature"
sensor_id = "temperature_01"

while True:
    payload = {
        "sensor_id": sensor_id,
        "data": {
            "temperature": round(random.uniform(25.0, 35.0), 2)
        }
    }
    try:
        response = requests.post(url, json=payload)
        print(f"[Temperature] Status: {response.status_code} | Response: {response.text}")
    except Exception as e:
        print(f"❌ Error sending temperature data: {e}")
    time.sleep(5)
