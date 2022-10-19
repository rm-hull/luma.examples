#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (c) 2014-2022 Richard Hull and contributors
# See LICENSE.rst for details.
# PYTHON_ARGCOMPLETE_OK

import sys
from pathlib import Path
from PIL import Image
from demo_opts import get_device

from luma.core.sprite_system import spritesheet, framerate_regulator


def main(num_iterations=sys.maxsize):
    data = {
        'image': str(Path(__file__).resolve().parent.joinpath(
            'images', f'jsw_{device.mode}.gif')
        ),
        'frames': {
            'width': 16,
            'height': 16,
            'regX': 0,
            'regY': 0
        },
        'animations': {
            'willy-right': {
                'frames': [8, 9, 10, 11],
                'next': "willy-right"
            },
            'willy-left': {
                'frames': [15, 14, 13, 12],
                'next': "willy-left"
            },
            'maria': {
                'frames': [4, 5, 4, 5, 4, 5, 4, 4, 4, 4, 4, 4, 6, 7, 7, 7, 6],
                'next': "maria",
                'speed': 0.5
            },
            'saw-left': {
                'frames': [191] * 128 + [56, 57, 58, 59] * 3,
                'next': "saw-left",
                'speed': 0.5
            },
            'hare-left': {
                'frames': [111, 110, 109, 108],
                'next': 'hare-left',
            }
        }
    }

    sheet = spritesheet(**data)
    regulator = framerate_regulator(fps=10)

    maria = sheet.animate('maria')
    willy = sheet.animate('willy-right')
    saw = sheet.animate('saw-left')
    hare = sheet.animate('hare-left')

    wx = 24
    hx = device.width
    clock = 0
    dx = 8

    while num_iterations > 0:
        with regulator:
            num_iterations -= 1

            background = Image.new(device.mode, device.size)
            background.paste(next(maria), (0, 0))
            background.paste(next(saw), (64, 0))
            background.paste(next(willy), (wx, 0))
            background.paste(next(hare), (hx, device.height - 16))
            device.display(background)
            clock += 1

            if clock % 4 == 0:
                wx += dx
                hx += -8

                if wx >= device.width - sheet.frames.width:
                    willy = sheet.animate('willy-left')
                    dx = -dx
                    wx = device.width - 24

                if wx <= 16:
                    willy = sheet.animate('willy-right')
                    dx = -dx
                    wx = 24

                if hx + sheet.frames.width <= 0:
                    hx = device.width


if __name__ == "__main__":
    try:
        device = get_device()
        main()
    except KeyboardInterrupt:
        pass
