from typing import Final
from sht3x.sht3x.sht3x import SHT3X

I2C_ADDRESS: Final[int] = 0x44


class SHT31(SHT3X):

    def __init__(self, bus_no: int):
        super().__init__(bus_no=bus_no,
                         address=I2C_ADDRESS,
                         model="SHT31")
