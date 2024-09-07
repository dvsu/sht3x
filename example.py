import json
import sys
from dataclasses import asdict

from smbus2 import SMBus

from sht3x import SHT31

bus = SMBus(1)
sensor = SHT31(bus)


while True:
    try:
        print(json.dumps(asdict(sensor.get_measurement()), indent=2))

    except KeyboardInterrupt:
        sys.exit(1)
