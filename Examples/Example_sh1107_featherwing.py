# Example_sh1107_featherwing.py
# Authored by: Mark Roberts (mdroberts1243)
# This example is for the Adafruit SH1107 128x64 OLED FeatherWing

import busio
import board
from adafruit_bus_device.i2c_device import I2CDevice
import adafruit_framebuf
import sh1107_i2c

# Native vertical framebuf... we will rotate the framebuffer to use the 
#        display horizontally later.
NATIVE_WIDTH = 64
NATIVE_HEIGHT = 128

# Desired horizontally-oriented framebuf for reference
WIDTH = 128
HEIGHT = 64

#
#  Some example code
#
with busio.I2C(board.SCL, board.SDA) as i2c:

    while not i2c.try_lock():                      # the SH1107 defaults to 0x3C (60)
        pass
    print("Found these I2C devices:", i2c.scan())  # confirm to the user the display is available
    i2c.unlock()

    device = I2CDevice(i2c, 60)                    # I2CDevice based driver, this manages the locks for us

    # natively the Featherwing is a 64 x 128 vertical display
    oled = sh1107_i2c.SH1107_I2C(NATIVE_WIDTH, NATIVE_HEIGHT, device)
    oled.rotation = 1     # orient as a horizontal display 128 x 64

    oled.fill(True)     # Fill routine to set the frame to all white
    oled.show()
    oled.fill_rect(0, 0, WIDTH, HEIGHT, False)   # Clear frame with a fill_rect
    oled.show()

    # default text output requires the font5x8.bin file to be available
    #      make sure the file is in your CIRCUITPY disk!
    print("Starting text string output -- 30 characters each")
    oled.text('123456789012345678901234567890', 0, 0, True, size=1)
    print("Second string")
    oled.text('123456789012345678901234567890', 0, 8, True, size=2)
    print("Third string")
    oled.text('123456789012345678901234567890', 0, 24, True, size=3)
    oled.show()

    print("Starting graphic primitive output")
    oled.rect(0, 0, WIDTH, HEIGHT, True) # outline the frame
    print("Line")
    oled.line(2, 2, WIDTH - 2, HEIGHT - 2, True) # diagonal line across the frame
    print("Three filled rectangles")
    oled.fill_rect(72, 0, 8, 8, True)
    oled.fill_rect(80, 8, 16, 16, True)
    oled.fill_rect(96, 24, 32, 32, True)
    print("Circle")
    oled.circle(64,32,30,True)  # a circle right in the middle almost full height
    oled.show()