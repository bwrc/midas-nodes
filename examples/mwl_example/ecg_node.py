#!/usr/bin/env python3
import sys
import numpy
import ecg_utilities

from midas.node import BaseNode
from midas import utilities as mu


# ECG processing node
class ECGNode(BaseNode):

    def __init__(self, *args):
        """ Initialize ECG node. """
        super().__init__(*args)
        self.metric_functions.append(self.mean_hr)

    def mean_hr(self, x, fs=500):
        """ Calculate the average heart rate 
            from the raw ECG signal x by first
            obtaining the RR-intervals using
            R-peak detection.
        """
        rr = ecg_utilities.detect_r_peaks(x['data'][0], fs)
        return 6e4 / numpy.mean(rr)

# Run the node from command line
if __name__ == '__main__':
    node = mu.midas_parse_config(ECGNode, sys.argv)
    if node:
        node.start()
        node.show_ui()
