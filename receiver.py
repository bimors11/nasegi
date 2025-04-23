from flask import Flask, request, render_template_string
import os
import json
from datetime import datetime

app = Flask(__name__)

# Folder tujuan penyimpanan
SAVE_FOLDER = "/home/bim/Tugas Akhir/Raw Data/"  # Ganti ke folder milik user kamu
os.makedirs(SAVE_FOLDER, exist_ok=True)

# Data sementara untuk ditampilkan di web
received_data = []

@app.route('/upload', methods=['POST'])
def upload():
    try:
        data = request.get_json(force=True)  # Pakai force=True agar tetap parsing walau header tidak sempurna

        # Validasi struktur JSON
        if not data or "sensor_id" not in data or "data" not in data or "soil_moisture" not in data["data"]:
            print("⚠️ Invalid JSON structure")
            return "Invalid JSON structure", 400

        # Simpan ke memori
        received_data.append(data)

        # Buat nama file berdasarkan waktu
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"data_{timestamp}.json"
        filepath = os.path.join(SAVE_FOLDER, filename)

        # Simpan ke file JSON
        with open(filepath, 'w') as f:
            json.dump(data, f, indent=4)

        print(f"✅ Data saved to {filepath}")
        return f"Data saved to {filepath}", 200
    except Exception as e:
        print(f"❌ Error occurred: {str(e)}")
        return f"Error occurred: {str(e)}", 500

@app.route('/')
def index():
    return render_template_string('''
        <html>
            <body>
                <h1>Data Received</h1>
                <table border="1">
                    <tr>
                        <th>Sensor ID</th>
                        <th>Soil Moisture</th>
                    </tr>
                    {% for entry in data %}
                    <tr>
                        <td>{{ entry['sensor_id'] }}</td>
                        <td>{{ entry['data']['soil_moisture'] }}</td>
                    </tr>
                    {% endfor %}
                </table>
            </body>
        </html>
    ''', data=received_data)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
