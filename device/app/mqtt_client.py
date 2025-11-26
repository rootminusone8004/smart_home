import paho.mqtt.client as mqtt


class MQTTClient:
    """Simple MQTT client for publishing messages"""

    def __init__(self, broker="localhost", port=1883):
        self.client = mqtt.Client()
        self.client.connect(broker, port, 60)

    def publish(self, topic, message):
        """Publish a message to a topic"""
        self.client.publish(topic, message)
