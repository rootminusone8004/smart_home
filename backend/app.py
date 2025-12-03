from flask import Flask, jsonify, render_template, request
import paho.mqtt.client as mqtt
import paho.mqtt.publish as publish
import threading

app = Flask(__name__)

latest_data = {"temperature": None, "humidity": None, "device": "device1"}

MQTT_BROKER = "localhost"
TOPIC_TEMP = "smarthome/device1/temperature"
TOPIC_HUM = "smarthome/device1/humidity"


def on_connect(client, userdata, flags, rc):
    print("MQTT connected with result code:", rc)
    client.subscribe(TOPIC_TEMP)
    client.subscribe(TOPIC_HUM)


def on_message(client, userdata, msg):
    payload = msg.payload.decode()
    topic = msg.topic

    if topic == TOPIC_TEMP:
        latest_data["temperature"] = float(payload)
    elif topic == TOPIC_HUM:
        latest_data["humidity"] = float(payload)


def mqtt_loop():
    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message

    client.connect(MQTT_BROKER, 1883, 60)
    client.loop_forever()


# Start MQTT thread
threading.Thread(target=mqtt_loop, daemon=True).start()


@app.route("/dashboard")
def dashboard():
    return render_template("dashboard.html")


@app.route("/sensor")
def get_sensor():
    return jsonify(latest_data)


@app.post("/relay/fan")
def relay_fan():
    data = request.get_json()
    state = data.get("state")  # "on" or "off"
    publish.single("smarthome/device1/relay/fan/set", state, hostname=MQTT_BROKER)
    return {"fan": state}


@app.post("/relay/light")
def relay_light():
    data = request.get_json()
    state = data.get("state")
    publish.single("smarthome/device1/relay/light/set", state, hostname=MQTT_BROKER)
    return {"light": state}


@app.route("/")
def home():
    return render_template("dashboard.html")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
