#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (c) 2014-2020 Richard Hull and contributors
# See LICENSE.rst for details.
# PYTHON_ARGCOMPLETE_OK

"""
A vertical scrolling demo, which should be familiar.
"""

import time
from pathlib import Path
from demo_opts import get_device
from luma.core.virtual import viewport
from luma.core.render import canvas
from PIL import Image


blurb = """


   Episode IV:
   A NEW HOPE

It is a period of
civil war. Rebel
spaceships, striking
from a hidden base,
have won their first
victory against the
evil Galactic Empire.

During the battle,
Rebel spies managed
to steal secret plans
to the Empire's ulti-
mate weapon, the
DEATH STAR, an armor-
ed space station with
enough power to des-
troy an entire planet.

Pursued by the
Empire's sinister
agents, Princess Leia
races home aboard her
starship, custodian
of the stolen plans
that can save her
people and restore
freedom to the
galaxy....
"""


def main():
    img_path = str(Path(__file__).resolve().parent.joinpath('images', 'starwars.png'))
    logo = Image.open(img_path)

    virtual = viewport(device, width=device.width, height=768)

    for _ in range(2):
        with canvas(virtual) as draw:
            draw.text((0, 0), "A long time ago", fill="white")
            draw.text((0, 12), "in a galaxy far", fill="white")
            draw.text((0, 24), "far away....", fill="white")

    time.sleep(5)

    for _ in range(2):
        with canvas(virtual) as draw:
            draw.bitmap((20, 0), logo, fill="white")
            for i, line in enumerate(blurb.split("\n")):
                draw.text((0, 40 + (i * 12)), text=line, fill="white")

    time.sleep(2)

    # update the viewport one position below, causing a refresh,
    # giving a rolling up scroll effect when done repeatedly
    for y in range(450):
        virtual.set_position((0, y))
        time.sleep(0.01)


if __name__ == "__main__":
    try:
        device = get_device()
        main()
    except KeyboardInterrupt:
        pass
