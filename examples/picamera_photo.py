#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (c) 2017-2022 Richard Hull and contributors
# See LICENSE.rst for details.
# PYTHON_ARGCOMPLETE_OK

"""
Capture photo with picamera and display it on a screen.

Requires picamera to be installed.
"""

import io
import sys
import time

from PIL import Image

from demo_opts import get_device

try:
    import picamera
except ImportError:
    print("The picamera library is not installed. Install it using 'sudo -H pip install picamera'.")
    sys.exit()


def main():
    cameraResolution = (1024, 768)
    displayTime = 5

    # create the in-memory stream
    stream = io.BytesIO()
    with picamera.PiCamera() as camera:
        # set camera resolution
        camera.resolution = cameraResolution

        print("Starting camera preview...")
        camera.start_preview()
        time.sleep(2)

        print("Capturing photo...")
        camera.capture(stream, format='jpeg', resize=device.size)

        print("Stopping camera preview...")
        camera.close()

        # "rewind" the stream to the beginning so we can read its content
        stream.seek(0)

        print(f"Displaying photo for {displayTime} seconds...")

        # open photo
        photo = Image.open(stream)

        # display on screen for a few seconds
        device.display(photo.convert(device.mode))
        time.sleep(displayTime)

        print("Done.")


if __name__ == "__main__":
    try:
        device = get_device()
        main()
    except KeyboardInterrupt:
        pass
