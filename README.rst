Introduction
============

CircuitPython framebuf driver for SH1107 OLED displays. I wrote this to get basic CircuitPython functionality with the "Adafruit FeatherWing OLED - 128x64 OLED Add-on For Feather - STEMMA QT / Qwiic".

This driver implements the `adafruit_framebuf interface <https://circuitpython.readthedocs.io/projects/framebuf/en/latest/>`__. Unfortunately, it is **not** a `displayio` driver for the SH1107. 

The SH1107 has a couple of quirks.  It doesn't have separate byte commands for setting column and row/page.  This makes it difficult to do a `displayio` driver for it. Also, it is natively oriented as a vertical 64 x 128 display so you need to rotate the frame buffer for a nice horizontal run of characters on the display.

Hardware
========
I tested this with the FeatherWing OLED mentioned above. I used it rotated in a horizontal orientation (128 x 64).  The Feather I used was the STM32F405.

Dependencies
=============
This driver depends on:

* `Adafruit CircuitPython <https://github.com/adafruit/circuitpython>`_
* `Bus Device <https://github.com/adafruit/Adafruit_CircuitPython_BusDevice>`_
* `Adafruit framebuf <https://github.com/adafruit/Adafruit_CircuitPython_framebuf>`_

**A note about Adafruit_framebuf:** It currently has an issue with rendering text in a rotated mode.  The text will be clipped at the native (narrow) width of the SH1107 OLED.  I submitted a PR to fix this issue: `Fix to framebuf for rotated text <https://github.com/adafruit/Adafruit_CircuitPython_framebuf/pull/37>`__ which you could download and use if not merged.

Please ensure all dependencies are available on the CircuitPython filesystem.
This is easily achieved by downloading
`the Adafruit library and driver bundle <https://github.com/adafruit/Adafruit_CircuitPython_Bundle>`_.

Usage Example
=============

.. code-block:: python3

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

Once the device, oled frame buffer and rotation are set up you can use any framebuf methods. These three lines use a filled rectangle to clear the screen, put a line of small text across the middle of the buffer and then display it on the screen:

.. code-block:: python3

	    oled.fill_rect(0, 0, WIDTH, HEIGHT, False)   # Clear frame with a fill_rect
	    oled.text('123456789012345678901234567890', 0, 28, True, size=1)
	    oled.show()
