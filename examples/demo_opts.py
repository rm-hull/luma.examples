# -*- coding: utf-8 -*-
# Copyright (c) 2014-17 Richard Hull and contributors
# See LICENSE.rst for details.

"""
Argument parser for examples.
"""

import sys
import logging
import argparse


# logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)-15s - %(message)s'
)
# ignore PIL debug messages
logging.getLogger('PIL').setLevel(logging.ERROR)


def load_config(fp):
    """
    Load device configuration from file.
    """
    args = []
    for line in fp.readlines():
        if line.strip() and not line.startswith('#'):
            args.append(line.replace("\n", ""))

    return args


def create_parser():
    """
    Create command-line argument parser.
    """
    parser = argparse.ArgumentParser(description='luma.examples arguments',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    parser.add_argument('--config', '-f', type=str, help='Load configuration settings from a file')
    parser.add_argument('--display', '-d', type=str, default='ssd1306', help='Display type, supports real devices or emulators', choices=["ssd1306", "ssd1322", "ssd1325", "ssd1331", "sh1106", "pcd8544", "max7219", "capture", "pygame", "gifanim"])
    parser.add_argument('--width', type=int, default=128, help='Width of the device in pixels')
    parser.add_argument('--height', type=int, default=64, help='Height of the device in pixels')
    parser.add_argument('--rotate', '-r', type=int, default=0, help='Rotation factor', choices=[0, 1, 2, 3])
    parser.add_argument('--interface', '-i', type=str, default='i2c', help='Serial interface type', choices=["i2c", "spi"])
    parser.add_argument('--i2c-port', type=int, default=1, help='I2C bus number')
    parser.add_argument('--i2c-address', type=str, default='0x3C', help='I2C display address')
    parser.add_argument('--spi-port', type=int, default=0, help='SPI port number')
    parser.add_argument('--spi-device', type=int, default=0, help='SPI device')
    parser.add_argument('--spi-bus-speed', type=int, default=8000000, help='SPI max bus speed (Hz)')
    parser.add_argument('--bcm-data-command', type=int, default=24, help='BCM pin for D/C RESET (SPI devices only)')
    parser.add_argument('--bcm-reset', type=int, default=25, help='BCM pin for RESET (SPI devices only)')
    parser.add_argument('--bcm-backlight', type=int, default=18, help='BCM pin for backlight (PCD8544 devices only)')
    parser.add_argument('--block-orientation', type=str, default='horizontal', help='Fix 90° phase error (MAX7219 LED matrix only)', choices=['horizontal', 'vertical'])
    parser.add_argument('--transform', type=str, default='scale2x', help='Scaling transform to apply (emulator only)', choices=["none", "identity", "scale2x", "smoothscale", "led_matrix", "seven_segment"])
    parser.add_argument('--scale', type=int, default=2, help='Scaling factor to apply (emulator only)')
    parser.add_argument('--mode', type=str, default='RGB', help='Colour mode (ssd1322, ssd1325 and emulator only)', choices=['1', 'RGB', 'RGBA'])
    parser.add_argument('--duration', type=float, default=0.01, help='Animation frame duration (gifanim emulator only)')
    parser.add_argument('--loop', type=int, default=0, help='Repeat loop, zero=forever (gifanim emulator only)')
    parser.add_argument('--max-frames', type=int, help='Maximum frames to record (gifanim emulator only)')

    try:
        import argcomplete
        argcomplete.autocomplete(parser)
    except ImportError:
        pass

    return parser


def get_device(actual_args=None):
    """
    Create and return the device.
    """
    if actual_args is None:
        actual_args = sys.argv[1:]

    parser = create_parser()
    args = parser.parse_args(actual_args)

    if args.config:
        with open(args.config, "r") as fp:
            config = load_config(fp)
            args = parser.parse_args(config + actual_args)

    if args.display in ('ssd1306', 'ssd1322', 'ssd1325', 'ssd1331', 'sh1106'):
        if args.interface not in ('i2c', 'spi'):
            parser.error('unknown interface %s' % args.interface)

        # luma.oled
        import luma.oled.device
        Device = getattr(luma.oled.device, args.display)
        try:
            if (args.interface == 'i2c'):
                from luma.core.serial import i2c
                serial = i2c(port=args.i2c_port, address=args.i2c_address)

            elif (args.interface == 'spi'):
                from luma.core.serial import spi
                serial = spi(port=args.spi_port,
                    device=args.spi_device,
                    bus_speed_hz=args.spi_bus_speed,
                    bcm_DC=args.bcm_data_command,
                    bcm_RST=args.bcm_reset)

            device = Device(serial, width=args.width, height=args.height,
                            rotate=args.rotate, mode=args.mode)
            return device

        except Exception as e:
            parser.error(e)

    elif args.display in ('pcd8544'):
        # luma.lcd
        import luma.lcd.device
        from luma.core.serial import spi
        Device = getattr(luma.lcd.device, args.display)
        try:
            serial = spi(port=args.spi_port,
                device=args.spi_device,
                bus_speed_hz=args.spi_bus_speed,
                bcm_DC=args.bcm_data_command,
                bcm_RST=args.bcm_reset)
            luma.lcd.device.backlight(bcm_LIGHT=args.bcm_backlight).enable(True)
            device = Device(serial, rotate=args.rotate)
            return device

        except Exception as e:
            parser.error(e)

    elif args.display in ('max7219'):
        # luma.led_matrix
        import luma.led_matrix.device
        from luma.core.serial import spi, noop
        Device = getattr(luma.led_matrix.device, args.display)
        try:
            serial = spi(port=args.spi_port,
                device=args.spi_device,
                bus_speed_hz=args.spi_bus_speed,
                gpio=noop())
            device = Device(serial, width=args.width, height=args.height,
                            rotate=args.rotate, block_orientation=args.block_orientation)
            return device

        except Exception as e:
            parser.error(e)

    elif args.display in ('capture', 'pygame', 'gifanim'):
        # luma.emulator
        import luma.emulator.device
        Device = getattr(luma.emulator.device, args.display)
        try:
            device = Device(**vars(args))
            return device

        except Exception as e:
            parser.error(e)

    else:
        parser.error('unknown display %s' % args.display)
