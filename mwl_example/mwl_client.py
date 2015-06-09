#!/usr/bin/env python3
import requests
import time
import sys


def print_physiological_state(bb_thr, rr_thr):
    """ Retrive and print activity metrics of the specified node. """
    # Format the metric requests
    addr = 'http://127.0.0.1:8080'
    bb_request = ('/eegnode/metric/'
                  '{"type":"brainbeat",'
                  '"channels":["ch0", "ch1"],'
                  '"time_window":[15]}')

    rr_request = ('/ecgnode/metric/'
                  '{"type":"mean_hr",'
                  '"channels":["ch0"],'
                  '"time_window":[15],'
                  '"arguments":[100]}')

    # Perform requests
    bb = requests.get(addr + bb_request).json()[0]['return']
    rr = requests.get(addr + rr_request).json()[0]['return']

    if bb > bb_thr and rr > rr_thr:
        mwl_class = '1'
    else:
        mwl_class = '0'

    print('%0.2f\t' % bb + '%0.2f\t' % rr + mwl_class)


def log_physiological_state(bb_thr=0.4, rr_thr=62):
    """ MIDAS physiological state logger. """
    try:
        while True:
            print_physiological_state(bb_thr, rr_thr)
            time.sleep(5)
    except KeyboardInterrupt:
        print("\nBye!")


if __name__ == '__main__':
    if len(sys.argv) == 3:
        log_physiological_state(float(sys.argv[1]), float(sys.argv[2]))
    else:
        log_physiological_state()
