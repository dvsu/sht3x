# Sensirion-SHT3X

Python-based driver for Sensirion SHT31/35 temperature and relative humidity sensor. Tested on Raspberry Pi Zero/ZeroW/3B+/4B

## Usage

For Sensirion SHT35

```python
import sys
import json
from smbus2 import SMBus
from dataclasses import asdict
from sht3x import SHT35
# for Sensirion SHT31
# from sht3x import SHT31 

# I2C bus 1
bus = SMBus(1)
sensor = SHT35(bus)

while True:
    try:
        print(json.dumps(asdict(sensor.get_measurement()), indent=2))

    except KeyboardInterrupt:
        sys.exit(1)

```

Example output

`get_measurement()`

```json
{
  "sensor": {
    "maker": "Sensirion",
    "model": "SHT35",
    "serial": null,
    "version": null
  },
  "measurements": [
    {
      "name": "temperature", 
      "unit": "C",
      "value": 27.95,
      "timestamp": "2023-10-01T01:23:45Z"
    }, 
    {
      "name": "temperature", 
      "unit": "F",
      "value": 82.3,
      "timestamp": "2023-10-01T01:23:45Z"
    },
    {
      "name": "relative_humidity",
      "unit": "%",
      "value": 54.98,
      "timestamp": "2023-10-01T01:23:45Z"
    }
  ]
}
```
