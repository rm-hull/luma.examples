#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (c) 2014-18 Richard Hull and contributors
# See LICENSE.rst for details.
# PYTHON_ARGCOMPLETE_OK

"""
10 PRINT is a book about a one-line Commodore 64 BASIC program, published in
November 2012. To paraphrase from http://10print.org/ "... a single line of
code—the extremely concise BASIC program for the Commodore 64 inscribed in the
title—and uses it as a lens through which to consider the phenomenon of creative
computing and the way computer programs exist in culture."
"""

import time
from random import random
from demo_opts import get_device
from luma.core.virtual import terminal


def main():
    term = terminal(device)

    term.println("10 PRINT CHR$(205.5+RND(1)); : GOTO 10")
    term.println()
    time.sleep(4)
    
    while True:
        ch = '/' if random() < 0.5 else '\\'
        term.puts(ch)
        term.flush()
        time.sleep(0.1)


if __name__ == "__main__":
    try:
        device = get_device()
        main()
    except KeyboardInterrupt:
        pass
