#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (c) 2019 Richard Hull and contributors
# See LICENSE.rst for details.
# PYTHON_ARGCOMPLETE_OK

import os
import multiprocessing
import time
import psutil
from datetime import datetime

from demo_opts import get_device
from luma.core.render import canvas

# Longer refresh rate the more history is shown
# If you set this to e.x. 30 sec you will get about 25 minutes of history on the graph
REFRESH_INTERVAL = 1

# FlipFlop blink variable
blnk = 1


def init_histogram():
    # HistogramSettings
    histogramResolution = 100
    histogramTime = []
    histogramData = []
    x = 106
    # Filling up the arrays for the histogram
    for pix in range(0, histogramResolution):
        x -= 2
        if x > 2:
            histogramTime.append(x)

    for timeLen in range(0, len(histogramTime)):
        histogramData.append(60)

    return histogramData, histogramTime


def main(device, histogramData, histogramTime):
    # Importing some global vars
    global blnk

    # Vars:
    # Getting system uptime
    sysUptime = datetime.now() - datetime.fromtimestamp(psutil.boot_time())

    # RAM bar
    minRamBarH = 15
    maxRamBarH = 25
    minRamBarW = 3
    maxRamBarW = 105
    ramStat = psutil.virtual_memory()
    ramTot = ramStat.total >> 20
    ramUsd = ramStat.used >> 20
    ramPerc = (ramUsd / ramTot) * 100
    ramBarWidth = (((100 - ramPerc) * (minRamBarW - maxRamBarW)) / 100) + maxRamBarW

    # Temp bar
    maxBarHeight = 60
    minBarHeight = 3
    try:
        with open("/sys/class/thermal/thermal_zone0/temp", "r") as temp:
            tmpCel = int(temp.read()[:2])
            tmpPercent = (tmpCel / 55) * 100

            height = (((100 - tmpPercent) * (maxBarHeight - minBarHeight)) / 100) + minBarHeight
    except:
        tmpCel = 0
        height = 0

    # Histogram graph
    cpuLoad = os.getloadavg()
    cpuPercent = (cpuLoad[0] / multiprocessing.cpu_count()) * 100
    minHistHeight = 60
    maxHistHeight = 30
    minHistLenght = 3
    maxHistLenght = 105
    histogramHeight = (((100 - cpuPercent) * (minHistHeight - maxHistHeight)) / 100) + maxHistHeight

    # Starting the canvas for the screen
    with canvas(device, dither=True) as draw:
        # Print
        # Drawing the outlines and legends:
        # Main Outline
        draw.rectangle(device.bounding_box, outline="white")

        # Histogram Outline
        draw.rectangle((minHistLenght, maxHistHeight, maxHistLenght, minHistHeight), outline="white")
        draw.rectangle((110, minBarHeight, 124, maxBarHeight), outline="white")
        draw.rectangle((104, minBarHeight, 110, minBarHeight + 8), fill="white")

        # Thermometer outline and legend
        draw.text((105, minBarHeight - 1), 'C', fill="black")

        # RAM bar outline and legend
        draw.rectangle((minRamBarW, minRamBarH, maxRamBarW, maxRamBarH))
        draw.text((maxRamBarW - 18, minRamBarH), 'RAM', fill="white")

        # System Uptime
        draw.text((3, 2), "Uptime: " + str(sysUptime)[:7], fill="white")

        # RAM usage bar
        if ramBarWidth < maxRamBarW:
            draw.rectangle((minRamBarW, minRamBarH, ramBarWidth, maxRamBarH), fill="white")
            if ramUsd < 100:
                draw.text((ramBarWidth - 11, minRamBarH), str(ramUsd), fill="black")
            else:
                draw.text((ramBarWidth - 17, minRamBarH), str(ramUsd), fill="black")
        else:
            draw.rectangle((minRamBarW, minRamBarH, maxRamBarW, maxRamBarH), fill="red")

        # Historgram
        histogramData.insert(0, histogramHeight)
        for htime in range(0, len(histogramTime) - 1):
            timePlusOne = htime + 1
            if histogramData[0] > maxHistHeight:
                draw.line((histogramTime[timePlusOne], histogramData[timePlusOne], histogramTime[htime], histogramData[htime]), fill="orange")
            else:
                histogramData[0] = maxHistHeight
                draw.text(((minHistLenght + maxHistLenght) / 2, (maxHistHeight + minHistHeight) / 2), "WARNING!", fill="white")
                draw.line((histogramTime[timePlusOne], histogramData[timePlusOne], histogramTime[htime], histogramData[htime]), fill="orange")

        histogramData.pop(len(histogramTime) - 1)
        draw.rectangle((minHistLenght, maxHistHeight, minHistLenght + 27, maxHistHeight + 13), fill="black", outline="white")
        draw.text((minHistLenght + 2, maxHistHeight + 2), "{0:.2f}".format(cpuLoad[0]), fill="white")

        # CPU Temperature
        if height > minBarHeight:
            draw.rectangle((112, height, 122, maxBarHeight), fill="gray")
            draw.rectangle((110, height, 124, height + 10), fill="white")
            draw.text((112, height), str(tmpCel), fill="black")
        else:
            draw.rectangle((110, minBarHeight, 124, maxBarHeight), outline="white")
            if blnk == 1:
                draw.rectangle((112, minBarHeight, 122, maxBarHeight), fill="gray")
                draw.rectangle((110, minBarHeight, 124, minBarHeight + 10), fill="white")
                draw.text((112, minBarHeight), str(tmpCel), fill="black")
                blnk = 0
            else:
                draw.rectangle((110, minBarHeight, 124, minBarHeight + 10), fill="black", outline="white")
                draw.text((112, minBarHeight), str(tmpCel), fill="white")
                blnk = 1


if __name__ == "__main__":
    device = get_device()
    histogramData, histogramTime = init_histogram()
    while True:
        main(device, histogramData, histogramTime)
        time.sleep(REFRESH_INTERVAL)
