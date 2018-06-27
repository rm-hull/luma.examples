#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (c) 2017 Richard Hull and contributors
# See LICENSE.rst for details.
# PYTHON_ARGCOMPLETE_OK

"""
Displays a matplotlib figure.
"""

from demo_opts import get_device
import matplotlib
matplotlib.use('module://backend_luma')

from pylab import *


def main():
    plot([1, 2, 3])
    show()


if __name__ == "__main__":
    try:
        device = get_device()
        main()
    except KeyboardInterrupt:
        pass