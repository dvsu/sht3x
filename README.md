# Sensirion-SHT3X

Python-based driver for Sensirion SHT31/35 temperature and relative humidity sensor. Tested on Raspberry Pi Zero/ZeroW/3B+/4B

## Usage

For Sensirion SHT35

```python
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
      "name": "temperature_celsius",
      "unit": "C",
      "value": 32.9,
      "datetime_utc": "2024-09-07T15:02:07Z",
      "timestamp_nanosec": 1725721327629009920
    },
    {
      "name": "temperature_fahrenheit",
      "unit": "F",
      "value": 91.21,
      "datetime_utc": "2024-09-07T15:02:07Z",
      "timestamp_nanosec": 1725721327629009920
    },
    {
      "name": "relative_humidity",
      "unit": "%",
      "value": 65.49,
      "datetime_utc": "2024-09-07T15:02:07Z",
      "timestamp_nanosec": 1725721327629009920
    }
  ]
}
```
