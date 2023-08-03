#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (c) 2017-2023 Richard Hull and contributors
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
from pathlib import Path
from demo_opts import get_device

import PIL

try:
    import av
except ImportError:
    print("The pyav library could not be found. Install it using 'sudo -H pip install av'.")
    sys.exit()


def main():
    video_path = str(Path(__file__).resolve().parent.joinpath('images', 'movie.mp4'))
    print(f'Loading {video_path}...')

    clip = av.open(video_path)

    for frame in clip.decode(video=0):
        print(f'{frame.index} ------')

        img = frame.to_image()
        if img.width != device.width or img.height != device.height:
            # resize video to fit device
            size = device.width, device.height
            img = img.resize(size, PIL.Image.LANCZOS)

        device.display(img.convert(device.mode))


if __name__ == "__main__":
    try:
        device = get_device()
        main()
    except KeyboardInterrupt:
        pass
