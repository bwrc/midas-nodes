import requests
import time


def get_node_list(addr):
    """ Returns a list of available nodes. """
    return requests.get(addr + '/status/nodes').json()


def map_value(value, current_min, current_max, new_min=0.0, new_max=1.0):
    new_value = (value - current_min) / (current_max - current_min)
    new_value = (new_value * new_max) + new_min
    return new_value


def constrain(value, min_val, max_val):
    """ Constrains value to a specific range. """
    if value < min_val:
        return min_val
    elif value > max_val:
        return max_val
    else:
        return value


def print_luminance_level(addr):
    """ Prints the current luminance level to the console. """
    # Format the metric request
    addr += ('/iotnode/metric/'
             '{"type":"mean_luminance",'
             '"channels":["ch0"],'
             '"time_window":[5]}')

    # Request metric
    value = float(requests.get(addr).json()[0]['return'])
    value = 120 - constrain(value, 10, 120)
    value = round(map_value(value, 10, 120, 0, 60))

    # Print response to the terminal
    print(time.ctime() +
          " " +
          '\033[93m' +
          '\033[1m' +
          ('*' * value) +
          '\033[0m')


def log_luminance(addr='http://127.0.0.1:8080'):
    """ MIDAS ambient light-level logger. """
    try:
        while True:
            node_list = get_node_list(addr)
            if 'iotnode' in node_list:
                print_luminance_level(addr)
            time.sleep(5)

    except KeyboardInterrupt:
        print("\nBye!")


if __name__ == '__main__':
    log_luminance()
