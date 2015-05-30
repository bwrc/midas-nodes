#!/usr/bin/env python3

import sys
from midas.node import BaseNode
from midas import utilities as mu
import qe_utils


# ------------------------------------------------------------------------------
# Create an Activity Node based on the Base Node
# ------------------------------------------------------------------------------
class QENode(BaseNode):
    """ MIDAS Activity Node """

    def __init__(self, *args):
        """ Initialize example node. """
        super().__init__(*args)
        self.metric_functions.append(qe_utils.current_app)
        self.metric_functions.append(qe_utils.idle_time)
        self.metric_functions.append(qe_utils.net_stat_sent)
        self.metric_functions.append(qe_utils.net_stat_recv)
        self.metric_functions.append(qe_utils.system_info)

# ------------------------------------------------------------------------------
# Run the node if started from the command line
# ------------------------------------------------------------------------------
if __name__ == '__main__':
    node = mu.midas_parse_config(QENode, sys.argv)
    if node is not None:
        node.start()
        node.show_ui()
# ------------------------------------------------------------------------------
# EOF
# ------------------------------------------------------------------------------
