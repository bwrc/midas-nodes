#!/usr/bin/env python3
import sys
import ecg_utilities

from midas.node import BaseNode
from midas import utilities as mu


# ECG processing node
class ECGNode(BaseNode):

    def __init__(self, *args):
        """ Initialize ECG node. """
        super().__init__(*args)
        self.metric_functions.append(ecg_utilities.hrv_mean_hr)

# Run the node from command line
if __name__ == '__main__':
    node = mu.midas_parse_config(ECGNode, sys.argv)
    if node:
        node.start()
        node.show_ui()
