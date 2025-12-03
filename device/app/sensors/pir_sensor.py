import RPi.GPIO as GPIO
import time


class PIRSensor:
    def __init__(self, pin=23):
        self.pin = pin
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.pin, GPIO.IN)
        self.motion_detected = False

    def read(self):
        """Returns True if motion is detected, else False"""
        self.motion_detected = GPIO.input(self.pin) == GPIO.HIGH
        return self.motion_detected
