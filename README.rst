`luma.core <https://github.com/rm-hull/luma.core>`__ **|** 
luma.examples **|** 
`luma.lcd <https://github.com/rm-hull/luma.lcd>`__ **|** 
`luma.led_matrix <https://github.com/rm-hull/luma.led_matrix>`__ **|** 
`luma.oled <https://github.com/rm-hull/luma.oled>`__ 

Luma.Examples
=============

.. image:: https://img.shields.io/maintenance/yes/2017.svg?maxAge=2592000

This is the companion repo for running examples against the `luma.oled <https://github.com/rm-hull/luma.oled>`_, 
`luma.lcd <https://github.com/rm-hull/luma.lcd>`_ and `luma.led_matrix <https://github.com/rm-hull/luma.led_matrix>`_ display drivers.

Installation instructions
-------------------------
Assuming you are using a Raspberry Pi (running Debian Jessie), follow the pre-requisites & 
instructions in the above repositories to wire up your display, then from a command-line::

  $ sudo usermod -a -G i2c,spi,gpio pi
  $ sudo apt-get install python-dev python-pip libfreetype6-dev libjpeg8-dev libsdl1.2-dev
  $ sudo -H pip install --upgrade pip
  $ sudo -H pip install --upgrade luma.oled luma.lcd luma.led_matrix
  
Log out and in again, clone this repository::

  $ git clone https://github.com/rm-hull/luma.examples
  $ cd luma.examples
  
Running the examples
--------------------
After cloning the repository, enter the ``examples`` directory and try running
the following examples:

===================== ================================================================
Example               Description
===================== ================================================================
3d_box.py             Rotating 3D box wireframe & color dithering
bounce.py             Display a bouncing ball animation and frames per second
carousel.py           Showcase viewport and hotspot functionality
clock.py              An analog clockface with date & time
colors.py             Color rendering demo
crawl.py              A vertical scrolling demo, which should be familiar
demo.py               Use misc draw commands to create a simple image
game_of_life.py       Conway's game of life
grayscale.py          Greyscale rendering demo
invaders.py           Space Invaders demo
maze.py               Maze generator
perfloop.py           Simple benchmarking utility to measure performance
pi_logo.py            Display the Raspberry Pi logo (loads image as .png)
savepoint.py          Example of savepoint/restore functionality
scrolling_pixelart.py Image dithering and viewport scrolling 
starfield.py          3D starfield simulation
sys_info.py           Display basic system information
terminal.py           Simple println capabilities
tv_snow.py            Example image-blitting
tweet_scroll.py       Using Twitter's Streaming API to display scrolling notifications
welcome.py            Unicode font rendering & scrolling
===================== ================================================================

By default, all the examples will asume I2C port 1, address ``0x3C`` and the
``ssd1306`` driver.  If you need to use a different setting, these can be
specified on the command line – each program can be invoked with a ``--help``
flag to show the options::

    $ python demo.py -h
    usage: demo.py [-h] [--config CONFIG]
                   [--display {ssd1306,ssd1322,ssd1325,ssd1331,sh1106,pcd8544,capture,pygame,gifanim}]
                   [--width WIDTH] [--height HEIGHT] [--rotate {0,1,2,3}]
                   [--interface {i2c,spi}] [--i2c-port I2C_PORT]
                   [--i2c-address I2C_ADDRESS] [--spi-port SPI_PORT]
                   [--spi-device SPI_DEVICE] [--spi-bus-speed SPI_BUS_SPEED]
                   [--bcm-data-command BCM_DATA_COMMAND] [--bcm-reset BCM_RESET]
                   [--bcm-backlight BCM_BACKLIGHT]
                   [--transform {none,identity,scale2x,smoothscale}]
                   [--scale SCALE] [--mode {1,RGB,RGBA}] [--duration DURATION]
                   [--loop LOOP] [--max-frames MAX_FRAMES]

    luma.examples arguments

    optional arguments:
      -h, --help            show this help message and exit
      --config CONFIG, -f CONFIG
                            Load configuration settings from a file (default:
                            None)
      --display {ssd1306,ssd1322,ssd1325,ssd1331,sh1106,pcd8544,capture,pygame,gifanim}, -d {ssd1306,ssd1322,ssd1325,ssd1331,sh1106,pcd8544,capture,pygame,gifanim}
                            Display type, supports real devices or emulators
                            (default: ssd1306)
      --width WIDTH         Width of the device in pixels (default: 128)
      --height HEIGHT       Height of the device in pixels (default: 64)
      --rotate {0,1,2,3}, -r {0,1,2,3}
                            Rotation factor (default: 0)
      --interface {i2c,spi}, -i {i2c,spi}
                            Serial interface type (default: i2c)
      --i2c-port I2C_PORT   I2C bus number (default: 1)
      --i2c-address I2C_ADDRESS
                            I2C display address (default: 0x3C)
      --spi-port SPI_PORT   SPI port number (default: 0)
      --spi-device SPI_DEVICE
                            SPI device (default: 0)
      --spi-bus-speed SPI_BUS_SPEED
                            SPI max bus speed (Hz) (default: 8000000)
      --bcm-data-command BCM_DATA_COMMAND
                            BCM pin for D/C RESET (SPI devices only) (default: 24)
      --bcm-reset BCM_RESET
                            BCM pin for RESET (SPI devices only) (default: 25)
      --bcm-backlight BCM_BACKLIGHT
                            BCM pin for backlight (PCD8544 devices only) (default:
                            18)
      --transform {none,identity,scale2x,smoothscale}
                            Scaling transform to apply (emulator only) (default:
                            scale2x)
      --scale SCALE         Scaling factor to apply (emulator only) (default: 2)
      --mode {1,RGB,RGBA}   Colour mode (emulator only) (default: RGB)
      --duration DURATION   Animation frame duration (gifanim emulator only)
                            (default: 0.01)
      --loop LOOP           Repeat loop, zero=forever (gifanim emulator only)
                            (default: 0)
      --max-frames MAX_FRAMES
                            Maximum frames to record (gifanim emulator only)
                            (default: None)

.. note::
   #. Substitute ``python3`` for ``python`` in the above examples if you are using python3.
   #. ``python-dev`` (apt-get) and ``psutil`` (pip/pip3) are required to run the ``sys_info.py`` 
      example. See `install instructions <https://github.com/rm-hull/luma.examples/blob/master/examples/sys_info.py#L3-L7>`_ for the exact commands to use.

Emulators
^^^^^^^^^
There are various display emulators available for running code against, for debugging
and screen capture functionality:

* The `luma.core.emulator.capture` device will persist a numbered PNG file to
  disk every time its ``display`` method is called.

* The `luma.core.emulator.gifanim` device will record every image when its ``display``
  method is called, and on program exit (or Ctrl-C), will assemble the images into an
  animated GIF.

* The `luma.core.emulator.pygame` device uses the `pygame` library to
  render the displayed image to a pygame display surface. 

Invoke the demos with::

  $ python examples/clock.py -d capture

or::

  $ python examples/clock.py -d pygame
  
.. note::
   *Pygame* is required to use any of the emulated devices, but it is **NOT**
   installed as a dependency by default, and so must be manually installed
   before using any of these emulation devices.

Documentation
-------------
Full documentation with installation instructions can be found in:

* https://luma-oled.readthedocs.io
* https://luma-lcd.readthedocs.io
* https://luma-led-matrix.readthedocs.io
* https://luma-core.readthedocs.io (coming soon)

License
-------
The MIT License (MIT)

Copyright (c) 2017 Richard Hull & Contributors

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
