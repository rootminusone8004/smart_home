import threading
import time
import concurrent.futures
from sensors.dht11_sensor import DHT11Sensor
from mqtt_client import MQTTClient
from controller import Controller
from sensors.pir_sensor import PIRSensor
from sensors.photoresistor import PhotoResistor

DEVICE_NAME = "device1"
MQTT_BROKER = "localhost"

light_sensor = PhotoResistor()

previous_motion = False
previous_light_status = "Default"

sensor = DHT11Sensor(pin=4)
pir_sensor = PIRSensor(pin=23)
controller = Controller()
mqtt_client = MQTTClient(
    controller=controller, broker=MQTT_BROKER, device_name=DEVICE_NAME
)

stop_event = threading.Event()


def safe_read_dht(timeout=0.3):
    with concurrent.futures.ThreadPoolExecutor(max_workers=1) as executor:
        future = executor.submit(sensor.read)
        try:
            return future.result(timeout=timeout)
        except concurrent.futures.TimeoutError:
            print("DHT11 read timeout")
            return None, None


def sensor_loop():
    while not stop_event.is_set():
        temperature, humidity = safe_read_dht()
        if temperature is not None and humidity is not None:
            mqtt_client.publish(
                f"smarthome/{DEVICE_NAME}/temperature", str(temperature)
            )
            mqtt_client.publish(f"smarthome/{DEVICE_NAME}/humidity", str(humidity))
            print(f"Published Temp={temperature}, Hum={humidity}")
        else:
            print("DHT11 read failed")

        light_status = light_sensor.read()
        mqtt_client.publish(f"smarthome/{DEVICE_NAME}/light", light_status)

        light_sensor_control(light_status)
        controller.update_lcd(temperature, humidity)

        time.sleep(1)


def pir_loop():
    global previous_motion
    while not stop_event.is_set():
        motion = pir_sensor.read()

        if motion and not previous_motion:
            # toggle light
            controller.set_light("off" if controller.relay_light.is_on else "on")
            mqtt_client.publish(f"smarthome/{DEVICE_NAME}/motion", "ON")
            print("Motion detected → toggled light")
        elif not motion:
            mqtt_client.publish(f"smarthome/{DEVICE_NAME}/motion", "OFF")

        previous_motion = motion
        time.sleep(2)


def light_sensor_control(light_status):
    global previous_light_status
    if light_status != previous_light_status:
        previous_light_status = light_status
        if light_status == "dark":
            controller.set_light("off")
            print("Darkness detected → Light ON")
        elif light_status == "bright":
            controller.set_light("on")
            print("Brightness detected → Light OFF")


mqtt_client.start()

# Start threads
t1 = threading.Thread(target=sensor_loop, daemon=True)
t2 = threading.Thread(target=pir_loop, daemon=True)
t1.start()
t2.start()

try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    print("\nShutting down gracefully...")
    stop_event.set()
    t1.join()
    t2.join()
