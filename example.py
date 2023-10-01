import sys
from smbus2 import SMBus
from datetime import datetime
from sht3x import SHT31

bus = SMBus(1)
sensor = SHT31(bus)


while True:
    try:
        print(
            datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ"),
            sensor.get_measurement(as_dict=True),
        )

    except KeyboardInterrupt:
        sys.exit(1)
