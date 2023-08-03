#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (c) 2014-2023 Richard Hull and contributors
# See LICENSE.rst for details.
# PYTHON_ARGCOMPLETE_OK

"""
Example of savepoint/restore functionality.
"""

import time
from demo_opts import get_device
from luma.core.virtual import history
from luma.core.render import canvas


def render_box(draw, idx, color):
    message = f"Nesting level: {idx}"
    # measure
    left, top, right, bottom = draw.textbbox((0, 0), message)
    width, height = right - left, bottom - top

    left = idx * 4
    right = left + width + 2
    top = idx * 4
    bottom = top + height + 2

    # draw
    draw.rectangle((left, top, right, bottom), outline="white", fill="black")
    draw.text((left + 2, top + 1), text=message, fill=color)


def main():
    colors = ["red", "green", "blue", "yellow", "magenta", "cyan"]
    hist = history(device)

    while True:

        # Phase 1: Redraw on a fresh canvas each loop
        for idx, color in enumerate(colors):
            with canvas(hist) as draw:
                render_box(draw, idx, color)

            hist.savepoint()
            time.sleep(1)

        while len(hist) > 0:
            # Drop every other save point
            hist.restore(drop=1)
            time.sleep(1)

        # Phase 2: Notice the difference with the above?
        # ... redraw on the *same* canvas
        c = canvas(hist)
        for idx, color in enumerate(colors):
            with c as draw:
                render_box(draw, idx, color)

            hist.savepoint()
            time.sleep(1)

        while len(hist) > 0:
            hist.restore()
            time.sleep(1)


if __name__ == "__main__":
    try:
        device = get_device()
        main()
    except KeyboardInterrupt:
        pass
