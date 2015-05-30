import requests
import time
import datetime


def log_iot():
    addr = ('http://127.0.0.1:8080/iotnode/metric/'
            '{"type":"mean_luminance", "channels":["ch0"], "time_window":[60]}')
    fh = open('/ukko/scratch/jari/iot_log.csv', 'w')
    try:
        while True:
            value = requests.get(addr).json()[0]['return']
            now = datetime.datetime.now()
            print(value)
            fh.writelines('%d\t%d\t%0.2f\n' % (now.hour, now.minute, value))
            fh.flush()
            time.sleep(60)
    except KeyboardInterrupt:
        fh.close()
        print("\nBye!")


if __name__ == '__main__':
    log_iot()
