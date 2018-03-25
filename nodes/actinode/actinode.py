#!/usr/bin/env python3

import sys
from midas.node import BaseNode
from midas import utilities as mu
import activity_utils 

# ------------------------------------------------------------------------------
# Create an Activity Node based on the Base Node
# ------------------------------------------------------------------------------
class ActivityNode(BaseNode):
    """ MIDAS Activity Node """

    def __init__(self, *args):
        """ Initialize example node. """
        super().__init__(*args)
        self.metric_functions.append(activity_utils.current_app)
        self.metric_functions.append(activity_utils.idle_time)


# ------------------------------------------------------------------------------
# Run the node if started from the command line
# ------------------------------------------------------------------------------
if __name__ == '__main__':
    node = mu.midas_parse_config(ActivityNode, sys.argv)
    if node is not None:
        node.start()
        node.show_ui()
# ------------------------------------------------------------------------------
# EOF
# ------------------------------------------------------------------------------
