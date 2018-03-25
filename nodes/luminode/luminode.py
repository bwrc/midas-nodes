#!/usr/bin/env python3

import sys
from midas.node import BaseNode
from midas import utilities as mu
import numpy as np


class LumiNode(BaseNode):

    def __init__(self, *args):
        """ Initialize example node. """
        super().__init__(*args)
        self.metric_functions.append(self.mean_luminance)

    def mean_luminance(self, x):
        """ Returns the average luminance """
        return np.mean(x['data'][0])


if __name__ == '__main__':
    node = mu.midas_parse_config(LumiNode, sys.argv)

    if node is not None:
        node.start()
        node.show_ui()
