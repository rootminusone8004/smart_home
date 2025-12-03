import RPi.GPIO as GPIO


class Relay:
    def __init__(self, pin, active_low=True):
        self.pin = pin
        self.active_low = active_low
        self.is_on = False

        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.pin, GPIO.OUT)
        self.off()  # default off at boot

    def on(self):
        GPIO.output(self.pin, GPIO.LOW if self.active_low else GPIO.HIGH)
        self.is_on = True

    def off(self):
        GPIO.output(self.pin, GPIO.HIGH if self.active_low else GPIO.LOW)
        self.is_on = False
