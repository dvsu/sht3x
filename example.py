import sys
from datetime import datetime
from sht3x import SHT35


sensor = SHT35(1)


while True:
    try:
        print(datetime.now(), sensor.get_measurement(as_dict=True))

    except KeyboardInterrupt:
        sys.exit(1)
