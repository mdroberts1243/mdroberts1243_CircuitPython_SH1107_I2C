# Driver adapted from multiple sources and study of datasheet
# Originally tested with Adafruit FeatherWing SH1107 128 x 64 OLED display
# Authored by: Mark Roberts (mdroberts1243)

import adafruit_framebuf
from board import *
from adafruit_bus_device.i2c_device import I2CDevice
import time

class SH1107_I2C(adafruit_framebuf.FrameBuffer):
    def __init__(self, width, height, i2c, *, external_vcc=False, reset=None):

        self.i2c_device = i2c
#        print("Passed device: ",self.i2c_device.i2c, self.i2c_device.device_address)
#        with self.i2c_device:
#            print("Seem to have the device")

        self.width = width
        self.height = height
        self.external_vcc = external_vcc
        self.pages = self.height // 8
        self.buffer = bytearray(self.pages * self.width)
        super().__init__(self.buffer, self.width, self.height, buf_format=adafruit_framebuf.MVLSB)
        self.init_display()

    def init_display(self):
#        print('Starting: init display')

        self.write_cmd([0xae])		    # display off, sleep mode
        self.write_cmd([0xdc, 0x02])	# display start line = 2 (POR = 0)
        self.write_cmd([0x81, 0x2f])    # contrast setting = 0x2f
        self.write_cmd([0x20])		    # page addressing mode (POR)
        self.write_cmd([0xa0])		    # segment remap = 0 (POR=0, down rotation)
        self.write_cmd([0xc0])		    # common output scan direction = 0 (0 to n-1 (POR=0))
        self.write_cmd([0xa8, 0x7f])	# multiplex ratio = 128 (POR)
        self.write_cmd([0xd3, 0x60])	# set display offset mode = 0x60
        self.write_cmd([0xd5, 0x51])	# divide ratio/oscillator: divide by 2, fOsc (POR)
        self.write_cmd([0xd9, 0x22])	# pre-charge/dis-charge period mode: 2 DCLKs/2 DCLKs (POR)
        self.write_cmd([0xdb, 0x35])	# VCOM deselect level = 0.770 (POR)
        self.write_cmd([0xb0])		    # set page address = 0 (POR)
        self.write_cmd([0xa4])		    # entire display off, retain RAM, normal status (POR)
        self.write_cmd([0xa6])		    # normal (not reversed) display

        self.fill(0)
        self.show()
        self.poweron()

    def show(self):
        for page in range(self.pages):
            buffer_i = page*self.width
            self.write_cmd([0xb0 | page])   # set page address
            self.write_cmd([0x00 | 2])      # set low column address
            self.write_cmd([0x10 | 0])      # set high column address
            self.write_data(bytearray(self.buffer[buffer_i:buffer_i+self.width]))

    def poweroff(self):
        self.write_cmd([0xae]) # display off, sleep mode

    def poweron(self):
        self.write_cmd([0xaf]) # display on

    def contrast(self, contrast):
        self.write_cmd([0x81, contrast]) # contrast is 0 to 255

    def invert(self, invert):
        self.write_cmd([0xa6 | (invert & 1)])

    def write_data(self, buf):
        with self.i2c_device:
            self.i2c_device.write(b'\x40'+buf) # 0x40 says everything after is data

    def write_cmd(self, cmd):
        with self.i2c_device:
            for cbyte in cmd:
                # every command byte is preceeded by 0x80
                self.i2c_device.write(bytearray([0x80,cbyte]))