#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
from setuptools import setup


def read_file(fname):
    with open(os.path.join(os.path.dirname(__file__), fname)) as r:
        return r.read()


README = read_file("README.rst")

needs_pytest = {'pytest', 'test', 'ptr'}.intersection(sys.argv)
pytest_runner = ['pytest-runner'] if needs_pytest else []
test_deps = ["mock", "pytest", "pytest-cov"]

setup(
    name="luma.examples",
    author="Richard Hull",
    author_email="richard.hull@destructuring-bind.org",
    description=("Examples for the luma libraries."),
    long_description=README,
    license="MIT",
    keywords="raspberry orange banana pi rpi opi sbc oled lcd led display screen spi i2c",
    url="https://github.com/rm-hull/luma.examples",
    install_requires=[
        "pillow>=4.0.0",
        "smbus2",
        "spidev",
        "RPi.GPIO"
    ],
    setup_requires=pytest_runner,
    tests_require=test_deps,
    extras_require={
        'docs': [
            'sphinx >= 1.5.1'
        ],
        'test': test_deps
    },
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Development Status :: 4 - Beta",
        "Intended Audience :: Education",
        "Intended Audience :: Developers",
        "Topic :: Education",
        "Topic :: System :: Hardware",
        "Topic :: System :: Hardware :: Hardware Drivers",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6"
    ]
)
