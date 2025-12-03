from actuators.relay import Relay
from actuators.lcd_display import LCDDisplay


class Controller:
    def __init__(self):
        # Relay pins (BCM)
        self.relay_fan = Relay(pin=17)
        self.relay_light = Relay(pin=27)
        self.lcd = LCDDisplay(i2c_addr=0x27)

    def set_fan(self, state: str):
        if state == "on":
            self.relay_fan.on()
        else:
            self.relay_fan.off()
        self.update_lcd()

    def set_light(self, state: str):
        if state == "on":
            self.relay_light.on()
        else:
            self.relay_light.off()
        self.update_lcd()

    def update_lcd(self, temperature=None, humidity=None):
        # Read sensor data if not provided
        temp_text = f"T:{temperature or '--'}C"
        hum_text = f"H:{humidity or '--'}%"
        fan_status = "Fan:ON" if self.relay_fan.is_on else "Fan:OFF"
        light_status = "Light:ON" if self.relay_light.is_on else "Light:OFF"

        self.lcd.write_line(f"{temp_text} {hum_text}", line=0)
        self.lcd.write_line(f"{fan_status} {light_status}", line=1)
