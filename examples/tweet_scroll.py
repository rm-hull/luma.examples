#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (c) 2014-2023 Richard Hull and contributors
# See LICENSE.rst for details.
# PYTHON_ARGCOMPLETE_OK

"""
Using Twitter's Streaming API to display scrolling notifications.

Instructions:
  1. Install tweepy, with 'sudo -H pip install tweepy'
  2. Get Twitter API keys:
     In order to access Twitter Streaming API, we need to get four pieces of
     information from Twitter: API key, API secret, Access token and Access
     token secret. Follow the steps below to get all four elements:
         - Create a twitter account if you do not already have one.
         - Go to https://apps.twitter.com/ and log in with your twitter
           credentials.
         - Click "Create New App"
         - Fill out the form, agree to the terms, and click "Create your
           Twitter application"
         - In the next page, click on "API keys" tab, and copy your "API
           key" and "API secret".
         - Scroll down and click "Create my access token", and copy your
           "Access token" and "Access token secret".
  3. Paste the four values into the variables below.
"""

consumer_key = "TWITTER_API_CONSUMER_KEY"
consumer_secret = "TWITTER_API_CONSUMER_SECRET"
access_token = "TWITTER_API_ACCESS_TOKEN"
access_token_secret = "TWITTER_API_ACCESS_TOKEN_SECRET"

search_terms = ['python']

import sys
import time
from pathlib import Path
from PIL import ImageFont

try:
    from Queue import Queue
except ImportError:
    from queue import Queue

from demo_opts import get_device
from luma.core.render import canvas
from luma.core.virtual import viewport


try:
    import tweepy
except ImportError:
    print("The tweepy library was not found. Run 'sudo -H pip install tweepy' to install it.")
    sys.exit()


def make_font(name, size):
    font_path = str(Path(__file__).resolve().parent.joinpath('fonts', name))
    return ImageFont.truetype(font_path, size)


def scroll_message(status, font=None, speed=1):
    author = f"@{status.author.screen_name}"
    full_text = f"{author}  {status.text}".replace("\n", " ")
    x = device.width

    # First measure the text size
    with canvas(device) as draw:
        left, top, right, bottom = draw.textbbox((0, 0), full_text, font)
        w, h = right - left, bottom - top

    virtual = viewport(device, width=max(device.width, w + x + x), height=max(h, device.height))
    with canvas(virtual) as draw:
        draw.text((x, 0), full_text, font=font, fill="white")
        draw.text((x, 0), author, font=font, fill="yellow")

    i = 0
    while i < x + w:
        virtual.set_position((i, 0))
        i += speed
        time.sleep(0.025)


class listener(tweepy.StreamListener):

    def __init__(self, queue):
        super(listener, self).__init__()
        self.queue = queue

    def on_status(self, status):
        self.queue.put(status)


device = get_device()
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)
queue = Queue()

if device.height >= 16:
    font = make_font("code2000.ttf", 12)
else:
    font = make_font("pixelmix.ttf", 8)

try:
    stream = tweepy.Stream(auth=api.auth, listener=listener(queue))
    stream.filter(track=search_terms, is_async=True)  # noqa: W606

    try:
        while True:
            status = queue.get()
            scroll_message(status, font=font)
    except KeyboardInterrupt:
        pass

finally:
    stream.disconnect()
