#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (c) 2017-18 Richard Hull and contributors
# See LICENSE.rst for details.
# PYTHON_ARGCOMPLETE_OK

"""
Capture continuous video stream with picamera and display it on a screen.

Requires picamera to be installed.
"""

import io
import sys
import time
import threading

from PIL import Image

from demo_opts import get_device

try:
    import picamera
except ImportError:
    print("The picamera library is not installed. Install it using 'sudo -H pip install picamera'.")
    sys.exit()


# create a pool of image processors
done = False
lock = threading.Lock()
pool = []


class ImageProcessor(threading.Thread):
    def __init__(self):
        super(ImageProcessor, self).__init__()
        self.stream = io.BytesIO()
        self.event = threading.Event()
        self.terminated = False
        self.start()

    def run(self):
        # this method runs in a separate thread
        global done
        while not self.terminated:
            # wait for an image to be written to the stream
            if self.event.wait(1):
                try:
                    self.stream.seek(0)

                    # read the image and display it on screen
                    photo = Image.open(self.stream)
                    device.display(photo.convert(device.mode))

                    # set done to True if you want the script to terminate
                    # at some point
                    # done=True
                finally:
                    # Reset the stream and event
                    self.stream.seek(0)
                    self.stream.truncate()
                    self.event.clear()

                    # return ourselves to the pool
                    with lock:
                        pool.append(self)


def streams():
    while not done:
        with lock:
            if pool:
                processor = pool.pop()
            else:
                processor = None
        if processor:
            yield processor.stream
            processor.event.set()
        else:
            # when the pool is starved, wait a while for it to refill
            time.sleep(0.1)


cameraResolution = (640, 480)
cameraFrameRate = 8
device = get_device()

with picamera.PiCamera() as camera:
    pool = [ImageProcessor() for i in range(4)]

    # set camera resolution
    camera.resolution = cameraResolution
    camera.framerate = cameraFrameRate

    print("Starting camera preview...")
    camera.start_preview()
    time.sleep(2)

    print("Capturing video...")
    try:
        camera.capture_sequence(streams(), use_video_port=True, resize=device.size)

        # shut down the processors in an orderly fashion
        while pool:
            with lock:
                processor = pool.pop()
            processor.terminated = True
            processor.join()
    except KeyboardInterrupt:
        pass
