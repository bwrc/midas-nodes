#!/usr/bin/env python3

import sys
from midas.node import BaseNode
from midas import utilities as mu
import numpy as np
import scipy.signal


class MyoNode(BaseNode):

    def __init__(self, *args):
        """ Initialize example node. """
        super().__init__(*args)
        self.metric_functions.append(self.emg_power)

    def emg_power(self, x):
        """ Returns the average power of the EMG signal """
        power = []
        for data in x['data']:
            f, p = 10*np.log10(scipy.signal.welch(data, fs=50.0))
            power.append(np.mean(p[np.bitwise_and(f >= 10.0, f <= 25.0)]))
        return power


if __name__ == '__main__':
    node = mu.midas_parse_config(MyoNode, sys.argv)

    if node is not None:
        node.start()
        node.show_ui()
