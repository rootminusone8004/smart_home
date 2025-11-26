import time
import board
import adafruit_dht


class DHT11Sensor:
    """CircuitPython DHT11 driver"""

    def __init__(self, pin=4):
        self.dht_device = adafruit_dht.DHT11(getattr(board, f"D{pin}"))

    def read(self):
        try:
            temperature = self.dht_device.temperature
            humidity = self.dht_device.humidity
            return temperature, humidity
        except Exception as e:
            print(f"Sensor read error: {e}")
            return None, None
