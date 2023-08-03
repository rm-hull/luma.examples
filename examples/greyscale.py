#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (c) 2014-2023 Richard Hull and contributors
# See LICENSE.rst for details.
# PYTHON_ARGCOMPLETE_OK

"""
Greyscale rendering demo.
"""

import time
from pathlib import Path
from demo_opts import get_device
from luma.core.render import canvas
from PIL import Image


def main():
    img_path = str(Path(__file__).resolve().parent.joinpath('images', 'balloon.png'))
    balloon = Image.open(img_path) \
        .transform(device.size, Image.AFFINE, (1, 0, 0, 0, 1, 0), Image.BILINEAR) \
        .convert("L") \
        .convert(device.mode)

    while True:
        # Image display
        device.display(balloon)
        device.display(balloon)
        time.sleep(5)

        # Greyscale
        shades = 16
        w = device.width / shades
        for _ in range(2):
            with canvas(device, dither=True) as draw:
                for i, color in enumerate(range(0, 256, shades)):
                    rgb = (color << 16) | (color << 8) | color
                    draw.rectangle((i * w, 0, (i + 1) * w, device.height), fill=rgb)

                left, top, right, bottom = draw.textbbox((0, 0), 'greyscale')
                size = right - left, bottom - top

                left = (device.width - size[0]) // 2
                top = (device.height - size[1]) // 2
                right = left + size[0]
                bottom = top + size[1]
                draw.rectangle((left - 1, top, right, bottom), fill="black")
                draw.rectangle(device.bounding_box, outline="white")
                draw.text((left, top), text="greyscale", fill="white")

        time.sleep(5)


if __name__ == "__main__":
    try:
        device = get_device()
        main()
    except KeyboardInterrupt:
        pass
