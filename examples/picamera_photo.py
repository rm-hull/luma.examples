"""
Capture photo to a PIL image -> OLED display.
"""

import io
import time

import picamera

from PIL import Image

from luma.core.serial import i2c
from luma.oled.device import ssd1306


def main():
    cameraResolution = (1024, 768)
    imageSize = (128, 64)

    # create OLED device
    serial = i2c()
    device = ssd1306(serial)

    # create the in-memory stream
    stream = io.BytesIO()
    with picamera.PiCamera() as camera:
        camera.resolution = cameraResolution
        print("Starting camera...")
        camera.start_preview()
        time.sleep(2)

        print("Capturing image...")
        camera.capture(stream, format='jpeg', resize=imageSize)

        print("Stopping camera...")
        camera.close()

        # "rewind" the stream to the beginning so we can read its content
        stream.seek(0)

        print("Displaying image....")
        photo = Image.open(stream).convert("RGBA")
        device.display(photo.convert(device.mode))

        time.sleep(5)
        print("Done.")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        pass

