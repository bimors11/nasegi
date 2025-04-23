from flask import Flask, request, render_template_string
import os
import json
from datetime import datetime

app = Flask(__name__)

# Ganti lokasi penyimpanan ke folder yang bisa dibaca CasaOS
BASE_FOLDER = "/DATA/SensorData/RawData"
SENSOR_FOLDERS = {
    "moisture": os.path.join(BASE_FOLDER, "Moisture"),
    "humidity": os.path.join(BASE_FOLDER, "Humidity"),
    "temperature": os.path.join(BASE_FOLDER, "Temperature"),
}

# Buat semua folder jika belum ada
for path in SENSOR_FOLDERS.values():
    os.makedirs(path, exist_ok=True)

# Menyimpan data sementara (untuk ditampilkan di web)
received_data = {
    "moisture": [],
    "humidity": [],
    "temperature": []
}

def save_data(sensor_type, expected_key):
    try:
        data = request.get_json(force=True)

        # Validasi format JSON
        if not data or "sensor_id" not in data or "data" not in data or expected_key not in data["data"]:
            print(f"⚠️ Invalid {sensor_type} JSON structure")
            return f"Invalid {sensor_type} JSON structure", 400

        # Simpan ke memori untuk web UI
        received_data[sensor_type].append(data)

        # Buat nama file berdasarkan timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{sensor_type}_{timestamp}.json"
        filepath = os.path.join(SENSOR_FOLDERS[sensor_type], filename)

        # Simpan data ke file JSON
        with open(filepath, 'w') as f:
            json.dump(data, f, indent=4)

        print(f"✅ {sensor_type.capitalize()} data saved to {filepath}")
        return f"{sensor_type.capitalize()} data saved to {filepath}", 200

    except Exception as e:
        print(f"❌ Error in {sensor_type}: {str(e)}")
        return f"Error occurred: {str(e)}", 500

# Endpoint untuk masing-masing sensor
@app.route('/upload/moisture', methods=['POST'])
def upload_moisture():
    return save_data("moisture", "soil_moisture")

@app.route('/upload/humidity', methods=['POST'])
def upload_humidity():
    return save_data("humidity", "humidity")

@app.route('/upload/temperature', methods=['POST'])
def upload_temperature():
    return save_data("temperature", "temperature")

# Web UI untuk melihat data sementara
@app.route('/')
def index():
    return render_template_string('''
        <html>
            <body>
                <h1>All Sensor Data</h1>

                <h2>Moisture</h2>
                <table border="1">
                    <tr><th>Sensor ID</th><th>Value</th></tr>
                    {% for entry in data['moisture'] %}
                    <tr><td>{{ entry['sensor_id'] }}</td><td>{{ entry['data']['soil_moisture'] }}</td></tr>
                    {% endfor %}
                </table>

                <h2>Humidity</h2>
                <table border="1">
                    <tr><th>Sensor ID</th><th>Value</th></tr>
                    {% for entry in data['humidity'] %}
                    <tr><td>{{ entry['sensor_id'] }}</td><td>{{ entry['data']['humidity'] }}</td></tr>
                    {% endfor %}
                </table>

                <h2>Temperature</h2>
                <table border="1">
                    <tr><th>Sensor ID</th><th>Value</th></tr>
                    {% for entry in data['temperature'] %}
                    <tr><td>{{ entry['sensor_id'] }}</td><td>{{ entry['data']['temperature'] }}</td></tr>
                    {% endfor %}
                </table>

            </body>
        </html>
    ''', data=received_data)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
