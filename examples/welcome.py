#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (c) 2014-2023 Richard Hull and contributors
# See LICENSE.rst for details.
# PYTHON_ARGCOMPLETE_OK

"""
Unicode font rendering & scrolling.
"""

import random
from pathlib import Path
from demo_opts import get_device
from luma.core.virtual import viewport, snapshot, range_overlap
from luma.core.sprite_system import framerate_regulator
from PIL import ImageFont


welcome = [
    u"Бзиала шәаабеит",
    u"Къеблагъ",
    u"Welkom",
    u"Bienvenue",
    u"Maayong pag-abot",
    u"Mayad-ayad nga pad-abot",
    u"Mir se vjên",
    u"እንኳን ደህና መጣህ።",
    u"Willkumme",
    u"أهلاً و سهل",
    u"مرحابة",
    u"Bienvenius",
    u"Բարի գալուստ!",
    u"আদৰণি",
    u'欢迎光临',
    u"歡迎光臨",
    u"ᑕᑕᐊᐧᐤ",
    u"Woé zɔ",
    u"Bula",
    u"Vælkomin",
    u"Buiti achüluruni",
    u"પધારો",
    u"ברוך הבא",
    u"Üdvözlet",
    u"ಸುಸ್ವಾಗತ",
    u"Приємаєме"
    u"Xoş gəlmişsiniz!",
    u"Salamat datang",
    u"Сәләм бирем!",
    u"Ongi etorri",
    u"Menjuah-juah!",
    u"স্বাগতম",
    u"Добре дошли",
    u"வாருங்கள்",
    u"Kíimak 'oolal",
    u"Märr-ŋamathirri",
    u"Benvinguts",
    u"Марша дагIийла шу",
    u"歡迎",
    u"Velkommen",
    u"Welcome",
    u"Wäljkiimen",
    u"კეთილი იყოს თქვენი",
    u"Καλώς Όρισες",
    u"Eguahé porá",
    u"Sannu da zuwa",
    u"Aloha",
    u"सवागत हैं",
    u"Selamat datang",
    u"Fáilte",
    u"ようこそ",
    u"Ирхитн эрҗәнәвидн",
    u"Witôj",
    u"សូម​ស្វាគមន៍",
    u"환영합니다",
    u"ຍິນດີຕ້ອນຮັບ",
    u"Swagatam",
    u"Haere mai",
    u"Тавтай морилогтун",
    u"خوش آمدید",
    u"Witam Cię",
    u"ਜੀ ਆਇਆ ਨੂੰ।",
    u"Bon vinuti",
    u"ยินดีต้อนรับ",
    u"Hoş geldiniz",
    u"Croeso",
    u"Bonvenon",
    u"Vitajte"
]

colors = [
    "lightpink", "pink", "crimson", "lavenderblush", "palevioletred", "hotpink",
    "deeppink", "mediumvioletred", "orchid", "thistle", "plum", "violet",
    "magenta", "fuchsia", "darkmagenta", "purple", "mediumorchid", "darkviolet",
    "darkorchid", "indigo", "blueviolet", "mediumpurple", "mediumslateblue",
    "slateblue", "darkslateblue", "lavender", "ghostwhite", "blue", "mediumblue",
    "midnightblue", "darkblue", "navy", "royalblue", "cornflowerblue",
    "lightsteelblue", "lightslategray", "slategray", "dodgerblue", "aliceblue",
    "steelblue", "lightskyblue", "skyblue", "deepskyblue", "lightblue",
    "powderblue", "cadetblue", "azure", "lightcyan", "paleturquoise", "cyan",
    "aqua", "darkturquoise", "darkslategray", "darkcyan", "teal",
    "mediumturquoise", "lightseagreen", "turquoise", "aquamarine",
    "mediumaquamarine", "mediumspringgreen", "mintcream", "springgreen",
    "mediumseagreen", "seagreen", "honeydew", "lightgreen", "palegreen",
    "darkseagreen", "limegreen", "lime", "forestgreen", "green", "darkgreen",
    "chartreuse", "lawngreen", "greenyellow", "darkolivegreen", "yellowgreen",
    "olivedrab", "beige", "lightgoldenrodyellow", "ivory", "lightyellow",
    "yellow", "olive", "darkkhaki", "lemonchiffon", "palegoldenrod", "khaki",
    "gold", "cornsilk", "goldenrod", "darkgoldenrod", "floralwhite", "oldlace",
    "wheat", "moccasin", "orange", "papayawhip", "blanchedalmond", "navajowhite",
    "antiquewhite", "tan", "burlywood", "bisque", "darkorange", "linen", "peru",
    "peachpuff", "sandybrown", "chocolate", "saddlebrown", "seashell", "sienna",
    "lightsalmon", "coral", "orangered", "darksalmon", "tomato", "mistyrose",
    "salmon", "snow", "lightcoral", "rosybrown", "indianred", "red", "brown",
    "firebrick", "darkred", "maroon", "white", "whitesmoke", "gainsboro",
    "lightgrey", "silver", "darkgray", "gray", "dimgray", "black"
]


def make_font(name, size):
    font_path = str(Path(__file__).resolve().parent.joinpath('fonts', name))
    return ImageFont.truetype(font_path, size)


def lerp_1d(start, end, n):
    delta = float(end - start) / float(n)
    for i in range(n):
        yield int(round(start + (i * delta)))
    yield end


def lerp_2d(start, end, n):
    x = lerp_1d(start[0], end[0], n)
    y = lerp_1d(start[1], end[1], n)

    try:
        while True:
            yield next(x), next(y)
    except StopIteration:
        pass


def pairs(generator):
    try:
        last = next(generator)
        while True:
            curr = next(generator)
            yield last, curr
            last = curr
    except StopIteration:
        pass


def infinite_shuffle(arr):
    copy = list(arr)
    while True:
        random.shuffle(copy)
        for elem in copy:
            yield elem


def make_snapshot(width, height, text, fonts, color="white"):

    def render(draw, width, height):
        t = text

        # measure text
        for font in fonts:
            left, top, right, bottom = draw.multiline_textbbox((0, 0), t, font)
            size = right - left, bottom - top
            if size[0] > width:
                t = text.replace(" ", "\n")
                left, top, right, bottom = draw.multiline_textbbox((0, 0), t, font)
                size = right - left, bottom - top
            else:
                break

        # draw text
        left = (width - size[0]) // 2
        top = (height - size[1]) // 2
        draw.multiline_text((left, top), text=t, font=font, fill=color,
                            align="center", spacing=-2)

    return snapshot(width, height, render, interval=10)


def random_point(maxx, maxy):
    return random.randint(0, maxx), random.randint(0, maxy)


def overlapping(pt_a, pt_b, w, h):
    la, ta = pt_a
    ra, ba = la + w, ta + h
    lb, tb = pt_b
    rb, bb = lb + w, tb + h
    return range_overlap(la, ra, lb, rb) and range_overlap(ta, ba, tb, bb)


def main():
    regulator = framerate_regulator(fps=30)
    fonts = [make_font("code2000.ttf", sz) for sz in range(24, 8, -2)]
    sq = device.width * 2
    virtual = viewport(device, sq, sq)

    color_gen = pairs(infinite_shuffle(colors))

    for welcome_a, welcome_b in pairs(infinite_shuffle(welcome)):
        color_a, color_b = next(color_gen)
        widget_a = make_snapshot(device.width, device.height, welcome_a, fonts, color_a)
        widget_b = make_snapshot(device.width, device.height, welcome_b, fonts, color_b)

        while True:
            posn_a = random_point(virtual.width - device.width, virtual.height - device.height)
            posn_b = random_point(virtual.width - device.width, virtual.height - device.height)
            if not overlapping(posn_a, posn_b, device.width, device.height):
                break

        virtual.add_hotspot(widget_a, posn_a)
        virtual.add_hotspot(widget_b, posn_b)

        for _ in range(30):
            with regulator:
                virtual.set_position(posn_a)

        for posn in lerp_2d(posn_a, posn_b, device.width // 4):
            with regulator:
                virtual.set_position(posn)

        virtual.remove_hotspot(widget_a, posn_a)
        virtual.remove_hotspot(widget_b, posn_b)


if __name__ == "__main__":
    try:
        device = get_device()
        main()
    except KeyboardInterrupt:
        pass
