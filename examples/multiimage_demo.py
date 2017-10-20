#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (c) 2014-17 Richard Hull and contributors
# See LICENSE.rst for details.
# PYTHON_ARGCOMPLETE_OK

"""
Scrolling artist + song and play/pause indicator
"""

import os
import sys
import time
from PIL import ImageFont, Image, ImageDraw
from demo_opts import get_device
from luma.core.render import canvas
from luma.core.multi_image import MultiImage, RenderedImage

titles = [
    ( "Bridge over troubled water", "Simon & Garfunkel" ),
    ( "Up", "R.E.M." ),
    ( "Wild Child", "Lou Reed & The Velvet Underground" ),
    ( "(Shake Shake Shake) Shake your body", "KC & The Sunshine Band" ),
]

class TextImage():
    def __init__(self, device, text, font):
        with canvas(device) as draw:
            w, h = draw.textsize(text, font)
        self.image = Image.new(device.mode, (w, h))
        draw = ImageDraw.Draw(self.image)
        draw.text((0,0), text, font=font, fill="white")
        del draw
        self.width = w
        self.height = h

class Synchroniser():
    def __init__(self):
        self.synchronised = {}

    def busy(self, task):
        self.synchronised[id(task)] = False
    
    def ready(self, task):
        self.synchronised[id(task)] = True

    def is_synchronised(self):
        for task in self.synchronised.iteritems():
            if task[1] == False:
                return False
        return True
    

class Scroller():
    WAIT_SCROLL = 1
    SCROLLING = 2
    WAIT_REWIND = 3
    WAIT_SYNC = 4
    def __init__(self, multi_image, rendered_image, scroll_delay, synchroniser):
        self.multi_image = multi_image
        self.speed = 1
        self.image_x_pos = 0
        self.rendered_image = rendered_image
        self.multi_image.add_image(rendered_image)
        self.max_pos = rendered_image.image.width - multi_image.image().width
        self.delay = scroll_delay
        self.ticks = 0
        self.state = self.WAIT_SCROLL
        self.synchroniser = synchroniser
        self.render()
        self.synchroniser.busy(self)
        self.cycles = 0
        self.must_scroll = self.max_pos > 0

    def __del__(self):
        self.multi_image.remove_image(self.rendered_image)

    def tick(self):

        # Repeats the following sequence:
        #  wait - scroll - wait - rewind -> sync with other scrollers -> wait
        if self.state == self.WAIT_SCROLL:
            if not self.is_waiting():
                self.cycles += 1
                self.state = self.SCROLLING
                self.synchroniser.busy(self)

        elif self.state == self.WAIT_REWIND:
            if not self.is_waiting():
                self.synchroniser.ready(self)
                self.state = self.WAIT_SYNC

        elif self.state == self.WAIT_SYNC:
            if self.synchroniser.is_synchronised():
                if self.must_scroll:
                    self.image_x_pos = 0
                    self.render()
                self.state = self.WAIT_SCROLL

        elif self.state == self.SCROLLING:
            if self.image_x_pos < self.max_pos:
                if self.must_scroll:
                    self.render()
                    self.image_x_pos += self.speed
            else:
                self.state = self.WAIT_REWIND

    def render(self):
        self.rendered_image.set_offset((self.image_x_pos, 0))

    def is_waiting(self):
        self.ticks += 1
        if self.ticks > self.delay:
            self.ticks = 0
            return False
        return True
        
    def get_cycles(self):
        return self.cycles


def make_font(name, size):
    font_path = os.path.abspath(os.path.join(
        os.path.dirname(__file__), 'fonts', name))
    return ImageFont.truetype(font_path, size)

# ------- main 

device = get_device()

if device.height >= 16:
    font  = make_font("code2000.ttf", 12)
else:
    font = make_font("pixelmix.ttf", 8)

mi = MultiImage(device, width=device.width, height=device.height)

try:
    while True:
        for title in titles:
            synchroniser = Synchroniser()
            ri = RenderedImage(TextImage(device, title[0], font).image, xy=(0,1))
            ri2 = RenderedImage(TextImage(device, title[1], font).image, xy=(0,30))
            song = Scroller(mi, ri, 100, synchroniser)
            artist = Scroller(mi, ri2, 100, synchroniser)
            cycles = 0

            while cycles < 3:
                artist.tick()
                song.tick()
                time.sleep(0.025)
                cycles = song.get_cycles()

                with canvas(device, background = mi.image()) as draw:
                    mi.refresh()
                    pass

            del artist
            del song

except KeyboardInterrupt:
    pass
