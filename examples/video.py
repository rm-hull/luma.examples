#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (c) 2017-18 Richard Hull and contributors
# See LICENSE.rst for details.
# PYTHON_ARGCOMPLETE_OK

"""
Display a video clip.

Make sure to install the av system packages:

  $ sudo apt-get install -y libavformat-dev libavcodec-dev libavdevice-dev libavutil-dev libswscale-dev libavresample-dev libavfilter-dev

And the pyav package (might take a while):

  $ sudo -H pip install av
"""

import sys
import os.path
from demo_opts import get_device

import PIL

try:
    import av
except ImportError:
    print("The pyav library could not be found. Install it using 'sudo -H pip install av'.")
    sys.exit()


def main():
    video_path = os.path.abspath(os.path.join(os.path.dirname(__file__),
        'images', 'movie.mp4'))
    print('Loading {}...'.format(video_path))

    clip = av.open(video_path)

    for frame in clip.decode(video=0):
        print('{} ------'.format(frame.index))

        img = frame.to_image()
        if img.width != device.width or img.height != device.height:
            # resize video to fit device
            size = device.width, device.height
            img = img.resize(size, PIL.Image.ANTIALIAS)

        device.display(img.convert(device.mode))


if __name__ == "__main__":
    try:
        device = get_device()
        main()
    except KeyboardInterrupt:
        pass
