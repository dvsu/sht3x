import sys

from smbus2 import SMBus

from sht3x import SHT31

bus = SMBus(1)
sensor = SHT31(bus)


while True:
    try:
        print(sensor.get_measurement().model_dump_json(indent=2))

    except KeyboardInterrupt:
        sys.exit(1)
