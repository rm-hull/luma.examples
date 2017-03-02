#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (c) 2017 Richard Hull and contributors
# See LICENSE.rst for details.

import os

import pytest

import luma.emulator.device

from demo_opts import load_config, get_device, create_parser


config_file = os.path.join(os.path.dirname(__file__),
    'resources', 'config-test.txt')


def test_create_parser():
    """
    create_parser returns an argument parser instance.
    """
    parser = create_parser()
    args = parser.parse_args(['-f', config_file])
    assert args.config == config_file


def test_load_config_parse():
    """
    load_config parses a text file and returns a list of arguments.
    """
    with open(config_file, "r") as fp:
        result = load_config(fp)

    assert result == [
        '--display=capture',
        '--width=800',
        '--height=8600',
        '--spi-bus-speed=16000000'
    ]


def test_get_device_missing_config():
    """
    Loading a missing config file throws an error.
    """
    with pytest.raises(IOError):
        get_device(['-f', 'foo'])


def test_get_device_good_config():
    """
    Loading a correct config file does not throw an error.
    """
    device = get_device(['-f', config_file])

    assert isinstance(device, luma.emulator.device.capture)


def test_get_device_unknown():
    """
    Load an unknown device.
    """
    with pytest.raises(SystemExit):
        get_device(['--display', 'foo'])


# luma.emulator

def test_get_device_emulator_capture():
    """
    Load the 'capture' emulator device.
    """
    device = get_device(['--display', 'capture'])

    assert isinstance(device, luma.emulator.device.capture)


def test_get_device_emulator_pygame():
    """
    Load the 'pygame' emulator device.
    """
    device = get_device(['--display', 'pygame'])

    assert isinstance(device, luma.emulator.device.pygame)


def test_get_device_emulator_gifanim():
    """
    Load the 'gifanim' emulator device.
    """
    device = get_device(['--display', 'gifanim'])

    assert isinstance(device, luma.emulator.device.gifanim)


# luma.led_matrix

def test_get_device_led_matrix_max7219():
    """
    Load the 'max7219' device.
    """
    #device = get_device(['--display', 'max7219'])

    #assert isinstance(device, luma.emulator.device.gifanim)
