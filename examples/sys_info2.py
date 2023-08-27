#!/usr/bin/python3
# -*- coding: utf-8 -*-


import os
import time
from datetime import datetime
from demo_opts import get_device
from luma.core.render import canvas
from PIL import ImageFont
import psutil
import subprocess as sp


def get_temp():
    temp = float(sp.getoutput("vcgencmd measure_temp").split('=')[1].split("'")[0])
    return temp


def get_cpu():
    return psutil.cpu_percent()


def get_mem():
    total_memory, used_memory, free_memory = map(
    int, os.popen('free -t -m').readlines()[-1].split()[1:])
    return used_memory / total_memory * 100


def get_disk():
    usage = psutil.disk_usage("/")
    return usage.used / usage.total * 100


def get_uptime():
    uptime = ("%s" % (datetime.now() - datetime.fromtimestamp(psutil.boot_time()))).split('.')[0]
    return "UpTime: %s" % (uptime)


def get_ip():
    ip = sp.getoutput("hostname -I").split(' ')[0]
    return "IP: %s" % (ip)


def format_percent(percent):
    return "%5.1f" %(percent)


def draw_text(draw, margin_x, line_num, text):
    draw.text((margin_x, margin_y_line[line_num]), text, font=font_default, fill="white")


def draw_bar(draw, line_num, percent):
    top_left_y = margin_y_line[line_num] + bar_margin_top;
    draw.rectangle((margin_x_bar, top_left_y, margin_x_bar + bar_width, top_left_y + bar_height), outline="white")
    draw.rectangle((margin_x_bar, top_left_y, margin_x_bar + bar_width * percent / 100, top_left_y + bar_height), fill="white")


def draw_bar_full(draw, line_num):
    top_left_y = margin_y_line[line_num] + bar_margin_top;
    draw.rectangle((margin_x_bar, top_left_y, margin_x_bar + bar_width_full, top_left_y + bar_height), fill="white")
    draw.text((65, top_left_y - 2), "100 %", font=font_full, fill="black")


def stats(device):
    with canvas(device) as draw:
        temp = get_temp()
        draw_text(draw, 0, 0, "Temp")
        draw_text(draw, margin_x_figure, 0, "%s'C" % (format_percent(temp)))

        cpu = get_cpu()
        draw_text(draw, 0, 1, "CPU")
        if cpu < 100 :
            draw_text(draw, margin_x_figure, 1, "%s %%" % (format_percent(cpu)))
            draw_bar(draw, 1, cpu)
        else :
            draw_bar_full(draw, 1)

        mem = get_mem()
        draw_text(draw, 0, 2, "Mem")
        if mem < 100 :
            draw_text(draw, margin_x_figure, 2, "%s %%" % (format_percent(mem)))
            draw_bar(draw, 2, mem)
        else :
            draw_bar_full(draw, 2)

        disk = get_disk()
        draw_text(draw, 0, 3, "Disk")
        if disk < 100 :
            draw_text(draw, margin_x_figure, 3, "%s %%" % (format_percent(disk)))
            draw_bar(draw, 3, disk)
        else :
            draw_bar_full(draw, 3)

        if datetime.now().second % (toggle_interval_seconds * 2) < toggle_interval_seconds :
            draw_text(draw, 0, 4, get_uptime())
        else :
            draw_text(draw, 0, 4, get_ip())


font_size = 12
font_size_full = 10
margin_y_line = [0, 13, 25, 38, 51]
margin_x_figure = 78
margin_x_bar = 31
bar_width = 52
bar_width_full = 95
bar_height = 8
bar_margin_top = 3
toggle_interval_seconds = 4


device = get_device()
font_default = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf', font_size)
font_full = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf', font_size_full)


while True:
    stats(device)
    time.sleep(0.5)

