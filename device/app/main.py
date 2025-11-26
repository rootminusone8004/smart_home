import time
from sensors.dht11_sensor import DHT11Sensor
from mqtt_client import MQTTClient

# Device configuration
DEVICE_NAME = "device1"  # Change to your preferred device name
MQTT_BROKER = "localhost"  # Or IP of broker if remote

# Initialize sensor and MQTT client
sensor = DHT11Sensor(pin=4)
mqtt_client = MQTTClient(broker=MQTT_BROKER)

print(f"Starting DHT11 MQTT publisher for {DEVICE_NAME}...")

try:
    while True:
        temperature, humidity = sensor.read()
        if temperature is not None and humidity is not None:
            mqtt_client.publish(
                f"smarthome/{DEVICE_NAME}/temperature", str(temperature)
            )
            mqtt_client.publish(f"smarthome/{DEVICE_NAME}/humidity", str(humidity))
            print(f"Published -> Temp: {temperature}°C, Humidity: {humidity}%")
        else:
            print("Failed to read from DHT11 sensor")

        time.sleep(5)  # Publish every 5 seconds

except KeyboardInterrupt:
    print("\nStopping device service...")
