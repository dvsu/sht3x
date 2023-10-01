from typing import Final
from smbus2 import SMBus
from .sht3x import SHT3X

I2C_ADDRESS: Final[int] = 0x44


class SHT31(SHT3X):
    def __init__(self, bus: SMBus):
        super().__init__(bus=bus, address=I2C_ADDRESS, model="SHT31")
