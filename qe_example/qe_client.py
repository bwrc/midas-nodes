import requests
import time


def get_node_list(addr):
    """ Returns a list of available nodes. """
    return requests.get(addr + '/status/nodes').json()


def print_activity_metrics(addr, node_name):
    """ Retrive and print activity metrics of the specified node. """
    # Format the metric request
    addr = addr + '/' + node_name + '/metric/'
    addr += ('[{"type":"current_app"},'
             '{"type":"idle_time"},'
             '{"type":"net_stat_sent"},'
             '{"type":"net_stat_recv"}]')
    responses = requests.get(addr).json()

    # Parse response and print result to the terminal
    s = time.ctime() + " " + node_name.ljust(10)
    for response in responses:
        value = response['return']
        if isinstance(value, str):
            s += value.ljust(15)
        else:
            value = value / 1e3
            if response['type'] == "idle_time" and value > 60:
                s += ('\033[91m' + str(value).ljust(15) + '\033[0m')
            else:
                s += str(value).ljust(15)

    print(s)


def log_activity(addr='http://127.0.0.1:8080'):
    """ MIDAS corporate activity logger. """
    try:
        while True:
            node_list = get_node_list(addr)
            for node in node_list:
                if (node_list[node]['status'] == 'online' and
                        node_list[node]['type'] == 'activity'):
                    print_activity_metrics(addr, node)
            time.sleep(5)

    except KeyboardInterrupt:
        print("\nBye!")


if __name__ == '__main__':
    log_activity()
