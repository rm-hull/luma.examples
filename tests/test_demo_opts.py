#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (c) 2017-2020 Richard Hull and contributors
# See LICENSE.rst for details.

"""
Tests for the :py:mod:`demo_opts` module.
"""

import sys
from pathlib import Path

from unittest.mock import patch, Mock
import pytest

import luma.emulator.device

from demo_opts import display_settings, get_device, cmdline


test_config_file = str(Path(__file__).resolve().parent.joinpath('resources', 'config-test.txt'))


def assertInError(msg, capsys):
    """
    Helper to find text in argparse error output message.
    """
    out, err = capsys.readouterr()
    assert msg in err


@patch('luma.core.__version__', '4.5.6')
def test_display_settings():
    """
    Summary including library version information is returned.
    """
    display_name = 'Awesome display'

    class Device:
        width = 120
        height = 80

    class DisplaySettingsConfig(object):
        display = display_name
        interface = 'USB'

    with patch('luma.core.cmdline.get_display_types') as mocka:
        mocka.return_value = {
            'superhdscreenz': [display_name, 'amazingscreen'],
            'emulator': ['x', 'y']
        }
        # set version nr for fake luma.superhdscreenz module
        luma_fake_lib = Mock()
        luma_fake_lib.__version__ = '1.2.3'
        with patch.dict('sys.modules', {'luma.superhdscreenz': luma_fake_lib}):

            result = display_settings(Device(), DisplaySettingsConfig())

            assert result == """Version: luma.superhdscreenz 1.2.3 (luma.core 4.5.6)
Display: Awesome display
Interface: USB
Dimensions: 120 x 80
------------------------------------------------------------"""


def test_get_device_config_file_missing():
    """
    Loading a missing config file throws an error.
    """
    with pytest.raises(IOError):
        get_device(['-f', 'foo'])


def test_get_device_config_file_success():
    """
    Loading a correct config file does not throw an error.
    """
    device = get_device(['-f', test_config_file])

    assert isinstance(device, luma.emulator.device.capture)


def test_get_device_unknown(capsys):
    """
    Load an unknown device.
    """
    test_args = [__name__, '--display', 'foo']
    with patch.object(sys, 'argv', test_args):
        with pytest.raises(SystemExit):
            get_device()

    assertInError("invalid choice: 'foo'", capsys)


# luma.emulator

def test_get_device_emulator_all():
    """
    Load an emulator device.
    """
    emulators = {
        'capture': luma.emulator.device.capture,
        'pygame': luma.emulator.device.pygame,
        'gifanim': luma.emulator.device.gifanim
    }
    for display, klass in emulators.items():
        device = get_device(['--display', display])
        assert isinstance(device, klass)


# luma.led_matrix

def test_get_device_led_matrix_all(capsys):
    """
    Load supported led_matrix devices one by one.
    """
    for display in cmdline.get_display_types().get('led_matrix'):
        try:
            get_device(['--display', display, '--interface', 'spi'])
        except SystemExit:
            assertInError('SPI device not found', capsys)
        except ImportError as e:
            pytest.skip(str(e))


# luma.lcd

def test_get_device_lcd_all(capsys):
    """
    Load supported lcd devices one by one.
    """
    for display in cmdline.get_display_types().get('lcd'):
        try:
            get_device(['--display', display])
        except SystemExit:
            try:
                assertInError('error: GPIO access not available', capsys)
            except:
                pass
        except ImportError as e:
            pytest.skip(str(e))


# luma.oled

def test_get_device_oled_all(capsys):
    """
    Load supported oled devices one by one.
    """
    for display in cmdline.get_display_types().get('oled'):
        with pytest.raises(SystemExit):
            get_device(['--display', display])

        assertInError('I2C device', capsys)


def test_get_device_oled_interface_unknown(capsys):
    """
    Get oled device with unknown interface.
    """
    with pytest.raises(SystemExit):
        get_device(['--display', 'ssd1306',
            '--interface', 'foo'])

    assertInError("argument --interface/-i: invalid choice: 'foo'", capsys)
