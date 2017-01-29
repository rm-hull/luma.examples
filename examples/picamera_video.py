import io
import time
import threading

import picamera

from PIL import Image

from luma.core.serial import i2c
from luma.oled.device import ssd1306


# Create a pool of image processors
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
        # This method runs in a separate thread
        global done
        while not self.terminated:
            # Wait for an image to be written to the stream
            if self.event.wait(1):
                try:
                    self.stream.seek(0)

                    # Read the image and do some processing on it
                    photo = Image.open(self.stream)
                    device.display(photo.convert(device.mode))
                    # Set done to True if you want the script to terminate
                    # at some point
                    #done=True
                finally:
                    # Reset the stream and event
                    self.stream.seek(0)
                    self.stream.truncate()
                    self.event.clear()
                    # Return ourselves to the pool
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
            # When the pool is starved, wait a while for it to refill
            time.sleep(0.1)

# create OLED device
serial = i2c()
device = ssd1306(serial)

with picamera.PiCamera() as camera:
    pool = [ImageProcessor() for i in range(4)]
    
    camera.resolution = (640, 480)
    imageSize = (128, 64)
    camera.framerate = 8
    camera.start_preview()
    time.sleep(2)
    camera.capture_sequence(streams(), use_video_port=True, resize=imageSize)

# Shut down the processors in an orderly fashion
while pool:
    with lock:
        processor = pool.pop()
    processor.terminated = True
    processor.join()
