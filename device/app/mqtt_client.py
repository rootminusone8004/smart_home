import paho.mqtt.client as mqtt


class MQTTClient:
    def __init__(self, controller, broker="localhost", device_name="device1"):
        self.controller = controller
        self.device_name = device_name

        self.topic_fan = f"smarthome/{device_name}/relay/fan/set"
        self.topic_light = f"smarthome/{device_name}/relay/light/set"

        self.client = mqtt.Client()

        # Assign callbacks
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message

        # Connect
        self.client.connect(broker, 1883, 60)

    def on_connect(self, client, userdata, flags, rc):
        print("MQTT connected with rc:", rc)

        # Subscribe to relay topics
        client.subscribe(self.topic_fan)
        client.subscribe(self.topic_light)

        print("Subscribed to:")
        print("  ", self.topic_fan)
        print("  ", self.topic_light)

    def on_message(self, client, userdata, msg):
        payload = msg.payload.decode().strip().lower()
        topic = msg.topic

        print(f"Received MQTT: {topic} -> {payload}")

        if topic == self.topic_fan:
            self.controller.set_fan(payload)

        elif topic == self.topic_light:
            self.controller.set_light(payload)

    def publish(self, topic, message):
        self.client.publish(topic, message)

    def start(self):
        """Non-blocking loop"""
        self.client.loop_start()
