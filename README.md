# Sensirion-SHT3X

Python-based driver for Sensirion SHT31/35 temperature and relative humidity sensor. Tested on Raspberry Pi Zero/ZeroW/3B+/4B

# Usage

For Sensirion SHT35

```python
import sys
from datetime import datetime
from sht3x import SHT35
# for Sensirion SHT31
# from sht3x import SHT31 

# I2C bus 1
sensor = SHT35(1)

while True:
    try:
        print(datetime.now(), sensor.get_measurement(as_dict=True))
        print(datetime.now(), sensor.get_full_reading(as_dict=True))
    except KeyboardInterrupt:
        sys.exit(1)

```

Example output

`get_measurement()`

```json
{
  "measurements": [
    {
      "name": "temperature", 
      "unit": "C",
      "value": 27.95
    }, 
    {
      "name": "temperature", 
      "unit": "F",
      "value": 82.3
    },
    {
      "name": "relative_humidity",
      "unit": "%",
      "value": 54.98
    }
  ]
}
```

`get_full_reading()`

```json
{
  "maker": "Sensirion",
  "model": "SHT35",
  "serial": null,
  "version": null,
  "timestamp": "2023-02-14T18:08:24Z",
  "measurements": [
    {
      "name": "temperature", 
      "unit": "C", 
      "value": 29.36
    }, 
    {
      "name": "temperature",
      "unit": "F",
      "value": 84.85
    }, 
    {
      "name": "relative_humidity",
      "unit": "%",
      "value": 52.62
    }
  ]
}
```