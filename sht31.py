from typing import Final
from sht3x.sht3x.sht3x import SHT3X

I2C_ADDRESS: Final[int] = 0x44


class SHT31(SHT3X):

    def __init__(self, bus_no: int):
        super().__init__(bus_no, I2C_ADDRESS)
