#!/usr/bin/env python2
# Copyright 2015
# Jari Torniainen <jari.torniainen@ttl.fi>
# Finnish Institute of Occupational Health
#
# This code is released under the MIT License
# http://opensource.org/licenses/mit-license.php
#
# Please see the file LICENSE for details.

import sys
sys.path.append('/home/uni/LSL/liblsl-Python')
import pylsl as lsl
from wiringx86 import GPIOEdison as GPIO
import binascii
import os
import time


def start_stream(sensor_pin=14, fs=10):

    # Setup the LSL stream
    uuid = binascii.b2a_hex(os.urandom(3))
    stream_info = lsl.StreamInfo('luminosity', 'analog', 1, fs, 'float32', uuid)
    stream_outlet = lsl.StreamOutlet(stream_info)

    # Setup GPIO
    gpio = GPIO(debug=False)
    gpio.pinMode(sensor_pin, gpio.ANALOG_INPUT)

    interval = 1.0 / fs

    try:
        while True:
            value = gpio.analogRead(sensor_pin)
            stream_outlet.push_sample([value])
            time.sleep(interval)

    except KeyboardInterrupt:
        print("\nCleaning up...")
        gpio.cleanup()

if __name__ == '__main__':
    start_stream()
