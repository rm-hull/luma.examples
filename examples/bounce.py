#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (c) 2014-18 Richard Hull and contributors
# See LICENSE.rst for details.
# PYTHON_ARGCOMPLETE_OK

"""
Display a bouncing ball animation and frames per second.

Attribution: https://github.com/rogerdahl/ssd1306/blob/master/examples/bounce.py
"""

import sys
import random

from demo_opts import get_device

import luma.core.render
from luma.core.sprite_system import framerate_regulator


class Ball(object):
    def __init__(self, w, h, radius, color):
        self._w = w
        self._h = h
        self._radius = radius
        self._color = color
        self._x_speed = (random.random() - 0.5) * 10
        self._y_speed = (random.random() - 0.5) * 10
        self._x_pos = self._w / 2.0
        self._y_pos = self._h / 2.0

    def update_pos(self):
        if self._x_pos + self._radius > self._w:
            self._x_speed = -abs(self._x_speed)
        elif self._x_pos - self._radius < 0.0:
            self._x_speed = abs(self._x_speed)

        if self._y_pos + self._radius > self._h:
            self._y_speed = -abs(self._y_speed)
        elif self._y_pos - self._radius < 0.0:
            self._y_speed = abs(self._y_speed)

        self._x_pos += self._x_speed
        self._y_pos += self._y_speed

    def draw(self, canvas):
        canvas.ellipse((self._x_pos - self._radius, self._y_pos - self._radius,
                       self._x_pos + self._radius, self._y_pos + self._radius), fill=self._color)


def main(num_iterations=sys.maxsize):
    colors = ["red", "orange", "yellow", "green", "blue", "magenta"]
    balls = [Ball(device.width, device.height, i * 1.5, colors[i % 6]) for i in range(10)]

    frame_count = 0
    fps = ""
    canvas = luma.core.render.canvas(device)

    regulator = framerate_regulator(fps=0)

    while num_iterations > 0:
        with regulator:
            num_iterations -= 1

            frame_count += 1
            with canvas as c:
                c.rectangle(device.bounding_box, outline="white", fill="black")
                for b in balls:
                    b.update_pos()
                    b.draw(c)
                c.text((2, 0), fps, fill="white")

            if frame_count % 20 == 0:
                fps = "FPS: {0:0.3f}".format(regulator.effective_FPS())


if __name__ == '__main__':
    try:
        device = get_device()
        main()
    except KeyboardInterrupt:
        pass
