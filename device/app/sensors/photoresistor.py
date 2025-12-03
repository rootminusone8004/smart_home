import RPi.GPIO as GPIO
import time


class PhotoResistor:
    def __init__(self, pin=22):
        self.pin = pin
        GPIO.setup(self.pin, GPIO.IN)

    def is_dark(self):
        # HIGH = light | LOW = dark (depends on module)
        return GPIO.input(self.pin) == GPIO.LOW

    def read(self):
        # Return boolean or convert to text
        return "dark" if self.is_dark() else "bright"
