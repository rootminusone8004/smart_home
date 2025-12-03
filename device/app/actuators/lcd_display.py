import smbus
import time

BACKLIGHT = 0x08
ENABLE = 0b00000100


# For standard 16x2 I2C LCD (PCF8574)
class LCDDisplay:
    def __init__(self, i2c_addr=0x27, bus=1):
        self.addr = i2c_addr
        self.bus = smbus.SMBus(bus)
        self.init_lcd()

    def init_lcd(self):
        # Initialize LCD (basic 4-bit mode)
        self.send_command(0x33)  # Initialize
        self.send_command(0x32)  # Set to 4-bit mode
        self.send_command(0x28)  # 2 line, 5x7 matrix
        self.send_command(0x0C)  # Turn cursor off
        self.send_command(0x06)  # Shift cursor right
        self.clear()

    def clear(self):
        self.send_command(0x01)
        time.sleep(0.002)

    def send_command(self, cmd):
        self.send_byte(cmd, 0)

    def send_data(self, data):
        self.send_byte(data, 1)

    def send_byte(self, data, mode):
        high = mode | (data & 0xF0) | BACKLIGHT
        low = mode | ((data << 4) & 0xF0) | BACKLIGHT
        self.bus.write_byte(self.addr, high)
        self.toggle_enable(high)
        self.bus.write_byte(self.addr, low)
        self.toggle_enable(low)

    def toggle_enable(self, data):
        self.bus.write_byte(self.addr, data | ENABLE)
        time.sleep(0.001)
        self.bus.write_byte(self.addr, data & ~ENABLE)
        time.sleep(0.001)

    def write_line(self, text, line=0):
        if line == 0:
            self.send_command(0x80)
        else:
            self.send_command(0xC0)
        text = text.ljust(16)
        for char in text:
            self.send_data(ord(char))
