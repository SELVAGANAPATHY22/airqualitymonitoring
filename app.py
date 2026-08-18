from flask import Flask, request, jsonify, render_template
from datetime import datetime

app = Flask(__name__)

# Store latest sensor data
latest_data = {
    "mq135": 0,
    "temperature": 0,
    "humidity": 0,
    "status": "WAITING",
    "time": "--:--:--"
}


# =====================================================
# DASHBOARD
# =====================================================

@app.route("/")
def dashboard():
    return render_template("dashboard.html")


# =====================================================
# ESP32 SENDS DATA HERE
# =====================================================

@app.route("/data", methods=["POST"])
def receive_data():

    global latest_data

    data = request.get_json()

    if data is None:
        return jsonify({
            "error": "Invalid JSON"
        }), 400

    latest_data["mq135"] = data.get("mq135", 0)
    latest_data["temperature"] = data.get("temperature", 0)
    latest_data["humidity"] = data.get("humidity", 0)
    latest_data["status"] = data.get("status", "UNKNOWN")

    latest_data["time"] = datetime.now().strftime("%H:%M:%S")

    print("Received data:")
    print(latest_data)

    return jsonify({
        "message": "Data received successfully",
        "data": latest_data
    })


# =====================================================
# DASHBOARD GETS LIVE DATA
# =====================================================

@app.route("/latest")
def latest():

    return jsonify(latest_data)


# =====================================================
# START SERVER
# =====================================================

if __name__ == "__main__":

    print("--------------------------------------")
    print("Ambient Air Quality Monitoring System")
    print("--------------------------------------")
    print("Server running on port 5000")
    print("--------------------------------------")

    app.run(
        host="0.0.0.0",
        port=5000,
        debug=True
    )