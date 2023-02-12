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

    except KeyboardInterrupt:
        sys.exit(1)

```

Example output

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
      "name": "relative humidity",
      "unit": "%",
      "value": 54.98
    }
  ]
}
```
