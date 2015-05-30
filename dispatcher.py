#!/usr/bin/env python3
import sys
from midas import utilities as mu
from midas.dispatcher import Dispatcher

# Run the dispatcher
dp = mu.midas_parse_config(Dispatcher, sys.argv)
dp.start()
