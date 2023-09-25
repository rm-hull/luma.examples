`luma.core <https://github.com/rm-hull/luma.core>`__ **|**
`luma.docs <https://github.com/rm-hull/luma.docs>`__ **|**
`luma.emulator <https://github.com/rm-hull/luma.emulator>`__ **|**
luma.examples **|**
`luma.lcd <https://github.com/rm-hull/luma.lcd>`__ **|**
`luma.led_matrix <https://github.com/rm-hull/luma.led_matrix>`__ **|**
`luma.oled <https://github.com/rm-hull/luma.oled>`__

Luma.Examples
=============

.. image:: https://github.com/rm-hull/luma.examples/workflows/luma.examples/badge.svg?branch=master
   :target: https://github.com/rm-hull/luma.examples/actions?workflow=luma.examples

This is the companion repo for running examples against the `luma.emulator <https://github.com/rm-hull/luma.emulator>`_,
`luma.oled <https://github.com/rm-hull/luma.oled>`_, `luma.lcd <https://github.com/rm-hull/luma.lcd>`_ and
`luma.led_matrix <https://github.com/rm-hull/luma.led_matrix>`_ display drivers.

Installation instructions
-------------------------
Assuming you are using a Raspberry Pi (running Debian Jessie or newer), follow the pre-requisites &
instructions in the above repositories to wire up your display, then from a command-line::

  $ sudo usermod -a -G i2c,spi,gpio pi
  $ sudo apt install python3-dev python3-pip python3-numpy libfreetype6-dev libjpeg-dev build-essential
  $ sudo apt install libsdl2-dev libsdl2-image-dev libsdl2-mixer-dev libsdl2-ttf-dev libportmidi-dev

Log out and in again and clone this repository::

  $ git clone https://github.com/rm-hull/luma.examples.git
  $ cd luma.examples

Finally, install the luma libraries using::

  $ sudo -H pip install -e .


Running the examples
--------------------
After cloning the repository, enter the ``examples`` directory and try running
one of the following examples listed below. For example::

  cd examples
  python3 3d_box.py

========================= ================================================================
Example                   Description
========================= ================================================================
3d_box.py                 Rotating 3D box wireframe & color dithering
animated_gif.py           Renders an animated GIF
bitstamp_ticker.py        Display the Bitcoin price at Bitstamp
bitstamp_realtime.py      Displays the latest Bitcoin trades in realtime at Bitstamp
bounce.py                 Display a bouncing ball animation and frames per second
carousel.py               Showcase viewport and hotspot functionality
chroma.py                 Trippy color rendering demo
clock.py                  An analog clockface with date & time
colors.py                 Color rendering demo
crawl.py                  A vertical scrolling demo, which should be familiar
demo.py                   Use misc draw commands to create a simple image
dotmatrixtool.py          Simple demo showing how to integrate output from http://dotmatrixtool.com
font_awesome.py           A meander through some awesome fonts
game_of_life.py           Conway's game of life
greyscale.py              Greyscale rendering demo
image_composition.py      Displays different song titles and scrolls them back and forth
invaders.py               Space Invaders demo
jetset_willy.py           Sprite animation framework demo
larson_hue.py             Alpha blending color demo
matrix.py                 The Matrix
maze.py                   Maze generator
perfloop.py               Simple benchmarking utility to measure performance
picamera_photo.py         Capture photo with picamera and display it on a screen
picamera_video.py         Capture continuous video stream and display it on a screen
pi_logo.py                Display the Raspberry Pi logo (loads image as .png)
runner.py                 Sprite animation framework demo
savepoint.py              Example of savepoint/restore functionality
scrolling_pixelart.py     Image dithering and viewport scrolling
sprite_animation.py       Using sprite maps for animation effects
starfield.py              3D starfield simulation
sys_histogram.py          Display system information including a rolling histogram
sys_info.py               Display basic system information
sys_info_extended.py      Display detailed system information in graph format
terminal.py               Simple println capabilities
tv_snow.py                Example image-blitting
tweet_scroll.py           Using Twitter's Streaming API to display scrolling notifications
video.py                  Display a video clip
weather.py                3-day weather forecasts from the BBC
welcome.py                Unicode font rendering & scrolling
========================= ================================================================

By default, all the examples will asume I2C port 1, address ``0x3C`` and the
``ssd1306`` driver.  If you need to use a different setting, these can be
specified on the command line – each program can be invoked with a ``--help``
flag to show the options::

    $ python3 examples/demo.py --help
    usage: demo.py [-h] [--config CONFIG] [--display DISPLAY] [--width WIDTH]
                    [--height HEIGHT] [--rotate ROTATION] [--interface INTERFACE]
                    [--i2c-port I2C_PORT] [--i2c-address I2C_ADDRESS]
                    [--spi-port SPI_PORT] [--spi-device SPI_DEVICE]
                    [--spi-bus-speed SPI_BUS_SPEED]
                    [--spi-transfer-size SPI_TRANSFER_SIZE]
                    [--spi-cs-high SPI_CS_HIGH] [--ftdi-device FTDI_DEVICE]
                    [--framebuffer-device FRAMEBUFFER_DEVICE] [--gpio GPIO]
                    [--gpio-mode GPIO_MODE]
                    [--gpio-data-command GPIO_DATA_COMMAND]
                    [--gpio-chip-select GPIO_CHIP_SELECT]
                    [--gpio-reset GPIO_RESET] [--gpio-backlight GPIO_BACKLIGHT]
                    [--gpio-reset-hold-time GPIO_RESET_HOLD_TIME]
                    [--gpio-reset-release-time GPIO_RESET_RELEASE_TIME]
                    [--block-orientation ORIENTATION] [--mode MODE]
                    [--framebuffer FRAMEBUFFER] [--num-segments NUM_SEGMENTS]
                    [--bgr] [--inverse] [--h-offset H_OFFSET]
                    [--v-offset V_OFFSET] [--backlight-active VALUE] [--debug]
                    [--transform TRANSFORM] [--scale SCALE] [--duration DURATION]
                    [--loop LOOP] [--max-frames MAX_FRAMES]

    luma.examples arguments

    options:
      -h, --help            show this help message and exit

    General:
      --config CONFIG, -f CONFIG
                            Load configuration settings from a file (default:
                            None)
      --display DISPLAY, -d DISPLAY
                            Display type, supports real devices or emulators.
                            Allowed values are: ssd1306, ssd1309, ssd1322,
                            ssd1362, ssd1322_nhd, ssd1325, ssd1327, ssd1331,
                            ssd1351, sh1106, sh1107, ws0010, winstar_weh, pcd8544,
                            st7735, st7789, ht1621, uc1701x, st7567, ili9341,
                            ili9486, ili9488, hd44780, max7219, ws2812, neopixel,
                            neosegment, apa102, unicornhathd, capture, gifanim,
                            pygame, asciiart, asciiblock, linux_framebuffer
                            (default: ssd1306)
      --width WIDTH         Width of the device in pixels (default: 128)
      --height HEIGHT       Height of the device in pixels (default: 64)
      --rotate ROTATION, -r ROTATION
                            Rotation factor. Allowed values are: 0, 1, 2, 3
                            (default: 0)
      --interface INTERFACE, -i INTERFACE
                            Interface type. Allowed values are: i2c, noop, spi,
                            gpio_cs_spi, bitbang, ftdi_spi, ftdi_i2c, pcf8574,
                            bitbang_6800 (default: i2c)

    I2C:
      --i2c-port I2C_PORT   I2C bus number (default: 1)
      --i2c-address I2C_ADDRESS
                            I2C display address (default: 0x3C)

    SPI:
      --spi-port SPI_PORT   SPI port number (default: 0)
      --spi-device SPI_DEVICE
                            SPI device (default: 0)
      --spi-bus-speed SPI_BUS_SPEED
                            SPI max bus speed (Hz) (default: 8000000)
      --spi-transfer-size SPI_TRANSFER_SIZE
                            SPI bus max transfer unit (bytes) (default: 4096)
      --spi-cs-high SPI_CS_HIGH
                            SPI chip select is high (gpio_cs_spi driver only)
                            (default: False)

    FTDI:
      --ftdi-device FTDI_DEVICE
                            FTDI device (default: ftdi://::/1)

    Linux framebuffer:
      --framebuffer-device FRAMEBUFFER_DEVICE
                            Linux framebuffer device (default: /dev/fd0)

    GPIO:
      --gpio GPIO           Alternative RPi.GPIO compatible implementation (SPI
                            interface only) (default: None)
      --gpio-mode GPIO_MODE
                            Alternative pin mapping mode (SPI interface only)
                            (default: None)
      --gpio-data-command GPIO_DATA_COMMAND
                            GPIO pin for D/C RESET (SPI interface only) (default:
                            24)
      --gpio-chip-select GPIO_CHIP_SELECT
                            GPIO pin for Chip select (GPIO_CS_SPI interface only)
                            (default: 24)
      --gpio-reset GPIO_RESET
                            GPIO pin for RESET (SPI interface only) (default: 25)
      --gpio-backlight GPIO_BACKLIGHT
                            GPIO pin for backlight (PCD8544, ST7735 devices only)
                            (default: 18)
      --gpio-reset-hold-time GPIO_RESET_HOLD_TIME
                            Duration to hold reset line active on startup
                            (seconds) (SPI interface only) (default: 0)
      --gpio-reset-release-time GPIO_RESET_RELEASE_TIME
                            Duration to pause for after reset line was made active
                            on startup (seconds) (SPI interface only) (default: 0)

    Misc:
      --block-orientation ORIENTATION
                            Fix 90° phase error (MAX7219 LED matrix only). Allowed
                            values are: 0, 90, -90, 180 (default: 0)
      --mode MODE           Colour mode (SSD1322, SSD1325 and emulator only).
                            Allowed values are: 1, RGB, RGBA (default: RGB)
      --framebuffer FRAMEBUFFER
                            Framebuffer implementation (SSD1331, SSD1322, ST7735,
                            ILI9341 displays only). Allowed values are:
                            diff_to_previous, full_frame (default:
                            diff_to_previous)
      --num-segments NUM_SEGMENTS
                            Sets the number of segments to when using the diff-to-
                            previous framebuffer implementation. (default: 4)
      --bgr                 Set if LCD pixels laid out in BGR (ST7735 displays
                            only). (default: False)
      --inverse             Set if LCD has swapped black and white (ST7735
                            displays only). (default: False)
      --h-offset H_OFFSET   Horizontal offset (in pixels) of screen to display
                            memory (ST7735 displays only). (default: 0)
      --v-offset V_OFFSET   Vertical offset (in pixels) of screen to display
                            memory (ST7735 displays only). (default: 0)
      --backlight-active VALUE
                            Set to "low" if LCD backlight is active low, else
                            "high" otherwise (PCD8544, ST7735 displays only).
                            Allowed values are: low, high (default: low)
      --debug               Set to enable debugging. (default: False)

    Emulator:
      --transform TRANSFORM
                            Scaling transform to apply (emulator only). Allowed
                            values are: identity, led_matrix, none, scale2x,
                            seven_segment, smoothscale (default: scale2x)
      --scale SCALE         Scaling factor to apply (emulator only) (default: 2)
      --duration DURATION   Animation frame duration (gifanim emulator only)
                            (default: 0.01)
      --loop LOOP           Repeat loop, zero=forever (gifanim emulator only)
                            (default: 0)
      --max-frames MAX_FRAMES
                            Maximum frames to record (gifanim emulator only)
                            (default: None)

.. note::
   #. ``python3-dev`` (apt-get) and ``psutil`` (pip/pip3) are required to run the ``sys_info.py``
      example. See `install instructions <https://github.com/rm-hull/luma.examples/blob/master/examples/sys_info.py#L10-L13>`_ for the exact commands to use.
   #. At runtime, ``luma.core`` enumerates which display drivers are present and dynamically constructs the list of ``--display`` options, therefore (for example) the ``capture``/``gifanim``/``pygame`` options will not show unless `luma.emulator` is installed

Emulators
^^^^^^^^^
There are various display emulators available for running code against, for debugging
and screen capture functionality:

* The `luma.emulator.device.capture` device will persist a numbered PNG file to
  disk every time its ``display`` method is called.

* The `luma.emulator.device.gifanim` device will record every image when its ``display``
  method is called, and on program exit (or Ctrl-C), will assemble the images into an
  animated GIF.

* The `luma.emulator.device.pygame` device uses the `pygame` library to
  render the displayed image to a pygame display surface.

After `installing luma.emulator <https://luma-emulator.readthedocs.io/en/latest/install.html>`_
you can invoke the demos with::

  $ python3 examples/clock.py --display pygame

or::

  $ python3 examples/clock.py --display gifanim

  $ python3 examples/starfield.py --display capture

Documentation
-------------
Full documentation with installation instructions can be found in:

* https://luma-oled.readthedocs.io
* https://luma-lcd.readthedocs.io
* https://luma-led-matrix.readthedocs.io
* https://luma-core.readthedocs.io
* https://luma-emulator.readthedocs.io

License
-------
The MIT License (MIT)

Copyright (c) 2017-2023 Richard Hull & Contributors

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
