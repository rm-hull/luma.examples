#!/usr/bin/python
#This is a simple system monitor that shows you CPU load histogram among other usefull stuff

from luma.core.interface.serial import i2c
from luma.core.render import canvas
from luma.oled.device import ssd1306
import os
import multiprocessing
import time
import psutil
from datetime import timedelta

#Setting up the screen
serial = i2c(port=0, address=0x3C)
device = ssd1306(serial)

#Longer refresh rate the more history is shown
#If you set this to e.x. 30 sec you will get about 25 minutes of history on the graph
refresh=1 #sec

#FlipFlop blink variable
blnk = 1

#HistogramSettings
histogramResolution=100
histogramTime = []
histogramData = []
x = 106
#Filling up the arrays for the histogram
for pix in range(0, histogramResolution):
    x -= 2
    if x > 2:
        histogramTime.append(x)

for timeLen in range(0,len(histogramTime)):
        histogramData.append(60)


def main():
        #Importing some global vars
        global blnk
        global histogramData
        global histogramTime
        #Starting the canvas for the screen
        with canvas(device, dither=True) as draw:
                #Vars:
                #Getting system uptime
                with open('/proc/uptime', 'r') as f:
                        uptime_seconds = float(f.readline().split()[0])
                        uptime_string = str(timedelta(seconds = uptime_seconds))
                #RAM bar
                minRamBarH=15
                maxRamBarH=25
                minRamBarW=3
                maxRamBarW=105
                ramStat=psutil.virtual_memory()
                ramTot=(ramStat.total >> 20)
                ramUsd=(ramStat.used  >> 20)
                ramPerc=((ramUsd / ramTot)*100)
                ramBarWidth=((((100 - ramPerc) * (minRamBarW - maxRamBarW)) /100) + maxRamBarW)
                #Temp bar
                temp=open ("/sys/class/thermal/thermal_zone0/temp","r")
                tmpCel= int(temp.read()[:2])
                tmpPercent= ((tmpCel / 55) * 100)
                minBarHeight= 60
                maxBarHeight= 3
                height= ((((100 - tmpPercent) * (minBarHeight - maxBarHeight)) / 100) + (maxBarHeight))
                #Histogram graph
                cpuLoad= os.getloadavg()
                cpuPercent= ((cpuLoad[0] / multiprocessing.cpu_count()) * 100)
                minHistHeight=60
                maxHistHeight=30
                minHistLenght=3
                maxHistLenght=105
                histogramHeight=((((100 - cpuPercent) * (minHistHeight - maxHistHeight)) / 100) + (maxHistHeight))

                #Print
                #Drawing the outlines and legends:
                draw.rectangle(device.bounding_box, outline="white") #Main
                draw.rectangle((minHistLenght,maxHistHeight , maxHistLenght,minHistHeight), outline="white") #Hist
                draw.rectangle(( 110, maxBarHeight, 124,minBarHeight ) , outline="white" ) # Therm
                draw.rectangle(( 104, maxBarHeight, 110,(maxBarHeight + 8)) , fill="white" ) # therm legend
                draw.text((105, (maxBarHeight - 1)),'C', fill="black") # therm legend
                draw.rectangle((minRamBarW,minRamBarH , maxRamBarW,maxRamBarH)) # RAM
                draw.text(((maxRamBarW - 18), (minRamBarH)), 'RAM', fill="white")       #Ram Legend

                #System Uptime
                draw.text((3,2), "Uptime: " + uptime_string[:7], fill="white" )

                #RAM usage bar
                if (ramBarWidth < maxRamBarW):
                        draw.rectangle((minRamBarW,minRamBarH, ramBarWidth,maxRamBarH) ,fill="white" )
                        if ramUsd < 100:
                                draw.text(((ramBarWidth - 11 ),minRamBarH), str(ramUsd),fill="black")
                        else:
                                draw.text(((ramBarWidth - 17 ),minRamBarH), str(ramUsd),fill="black")
                else:
                        draw.rectangle((minRamBarW,minRamBarH, maxRamBarW,maxRamBarH) ,fill="red" )

                #Historgram
                histogramData.insert(0, histogramHeight)
                for time in range(0,(len(histogramTime)-1)):
                        timePlusOne=(time + 1)
                        if (histogramData[0] > maxHistHeight):
                                draw.line((histogramTime[timePlusOne],histogramData[timePlusOne] , histogramTime[time],histogramData[time]), fill="orange")
                        else:
                                histogramData[0]=maxHistHeight
                                draw.text((((minHistLenght+maxHistLenght)/2), ((maxHistHeight + minHistHeight)/2)), "WARNING!", fill="white")
                                draw.line((histogramTime[timePlusOne],histogramData[timePlusOne] , histogramTime[time],histogramData[time]), fill="orange")
                histogramData.pop((len(histogramTime)-1))
                draw.rectangle((minHistLenght,maxHistHeight , (minHistLenght+27),(maxHistHeight+13)), fill="black", outline="white") #Hist
                draw.text(((minHistLenght+2), (maxHistHeight+2)), str(cpuLoad[0]), fill="white")

                #CPU Temperature
                if (height > maxBarHeight):
                        draw.rectangle(( 112, height, 122,minBarHeight ) , fill="gray" )
                        draw.rectangle(( 110, height, 124,(height+10) ) , fill="white" )
                        draw.text((112, height), str(tmpCel), fill="black")
                else:
                        draw.rectangle(( 110, maxBarHeight, 124,minBarHeight ) , outline="white" )
                        if blnk == 1:
                                draw.rectangle(( 112, maxBarHeight, 122,minBarHeight ) , fill="gray" )
                                draw.rectangle(( 110, maxBarHeight, 124,(maxBarHeight+10) ) , fill="white")
                                draw.text((112, maxBarHeight), str(tmpCel), fill="black")
                                blnk = 0
                        else:
                                draw.rectangle(( 110, maxBarHeight, 124,(maxBarHeight+10) ) , fill="black", outline="white" )
                                draw.text((112, maxBarHeight), str(tmpCel), fill="white")
                                blnk = 1

#END main

#Infinite loop
while True:
        main()
        time.sleep(refresh)
