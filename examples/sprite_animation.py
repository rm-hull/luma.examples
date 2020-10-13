#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (c) 2014-2020 Richard Hull and contributors
# See LICENSE.rst for details.
# PYTHON_ARGCOMPLETE_OK

"""
Sprite animation
"""

import time
from pathlib import Path
from demo_opts import get_device
from PIL import Image


def mickey():
    img_path = str(Path(__file__).resolve().parent.joinpath('images', 'mickey-sprite.png'))
    spritemap = Image.open(img_path).convert("RGBA")

    background = Image.new("RGBA", device.size, "black")

    w = 256
    h = 308
    scale = device.height / float(h)
    new_size = (int(scale * w), device.height)
    for _ in range(5):
        frame = 0
        while frame < 40:

            x = w * (frame % 8)
            y = h * (frame // 8)

            img = spritemap.crop((x, y, x + w, y + h)).resize(new_size)

            offset = (device.width - img.width) // 2
            background.paste(img, (offset, 0))
            device.display(background.convert(device.mode))

            frame += 1
            time.sleep(0.05)


def explosion():
    img_path = str(Path(__file__).resolve().parent.joinpath('images', 'explosion.png'))
    spritemap = Image.open(img_path).convert("RGBA")

    background = Image.new("RGBA", device.size, "black")

    w = 50
    h = 54
    offset = (device.width - w) // 2
    frame = 0
    while frame < 40:

        x = w * (frame % 10)
        y = h * (frame // 10)

        img = spritemap.crop((x, y, x + w, y + h))
        background.paste(img, (offset, 0))
        device.display(background.convert(device.mode))

        frame += 1
        time.sleep(0.1)


if __name__ == "__main__":
    try:
        device = get_device()
        while True:
            mickey()
            explosion()
            time.sleep(4)
    except KeyboardInterrupt:
        pass
