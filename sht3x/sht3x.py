import sys
from time import sleep, time
from traceback import print_exc
from dataclasses import asdict
from typing import Final, Literal, Optional
from smbus2 import SMBus
from sht3x.models import Measurement, SensorData, SensorInfo

CLK_STRETCHING_MODE = Literal["ENABLED", "DISABLED"]
REPEATABILITY_SETTING = Literal["HIGH", "MEDIUM", "LOW"]

CMD_READ_STATUS_REG: Final[list[int]] = [0xF3, 0x2D]
CMD_CLEAR_STATUS_REG: Final[list[int]] = [0x30, 0x41]

REG_BASE: Final[int] = 0x00

LEN_STATUS_REG: Final[int] = 3
LEN_TEMP_HUMI_DATA: Final[int] = 6

CLK_STRETCHING: Final[dict[CLK_STRETCHING_MODE, int]] = {
    "ENABLED": 0x2C,
    "DISABLED": 0x24
}

REPEATABILITY: Final[dict[CLK_STRETCHING_MODE, dict[REPEATABILITY_SETTING, int]]] = {
    # Repeatability with clock stretching enabled
    "ENABLED": {
        "HIGH": 0x06,
        "MEDIUM": 0x0D,
        "LOW": 0x10
    },
    # Repeatability with clock stretching disabled
    "DISABLED": {
        "HIGH": 0x00,
        "MEDIUM": 0x0B,
        "LOW": 0x16
    },
}


class SHT3X:

    def __init__(self, bus_no: int, address: int):
        self.__tracker: int = 0
        self.__bus: SMBus = None
        self.__verbose: bool = True
        try:
            self.__bus = SMBus(bus_no)

        except FileNotFoundError:
            print_exc(limit=2, file=sys.stdout)
            sys.exit(1)

        self.__address = address

        # try:
        #     self.__bus.read_byte_data(self.__address, 0)

        # except OSError:
        #     print_exc(limit=2, file=sys.stdout)
        #     sys.exit(1)

        self.__clock_stretching = CLK_STRETCHING["DISABLED"]
        self.__repeatability = REPEATABILITY["DISABLED"]["HIGH"]
        self.read_status_register()

    def crc_check(self, data: list, checksum: int) -> bool:
        return self.crc_calc(data) == checksum

    def crc_calc(self, data: list) -> int:
        crc = 0xFF
        for i in range(2):
            crc ^= data[i]
            for _ in range(8, 0, -1):
                if crc & 0x80:
                    crc = (crc << 1) ^ 0x31
                else:
                    crc = crc << 1

        # The checksum only contains 8-bit, so the calculated value will be masked with 0xFF
        return (crc & 0x0000FF)

    def alert_pending_status(self, data: int) -> str:
        status = (data & 0b1000000000000000) >> 15

        if not self.__verbose:
            return str(status)

        return "At least one pending alert" if status else "No pending alerts"

    def heater_status(self, data: int) -> str:
        status = (data & 0b0010000000000000) >> 13

        if not self.__verbose:
            return str(status)

        return "Heater ON" if status else "Heater OFF"

    def humidity_tracking_status(self, data: int) -> str:
        status = (data & 0b0000100000000000) >> 11

        if not self.__verbose:
            return str(status)

        return "Alert" if status else "No alert"

    def temperature_tracking_status(self, data: int) -> str:
        status = (data & 0b0000010000000000) >> 10

        if not self.__verbose:
            return str(status)

        return "Alert" if status else "No alert"

    def system_reset_status(self, data: int) -> str:
        status = (data & 0b0000000000010000) >> 4

        if not self.__verbose:
            return str(status)

        return "Reset detected" if status else "No reset detected"

    def command_status(self, data: int) -> str:
        status = (data & 0b0000000000000010) >> 1

        if not self.__verbose:
            return str(status)

        return "Last command not processed" if status else "Last command executed successfully"

    def write_data_checksum_status(self, data: int) -> str:
        status = data & 0b0000000000000001

        if not self.__verbose:
            return str(status)

        return "Failed" if status else "Correct"

    def read_status_register(self):
        self.__bus.write_i2c_block_data(self.__address, CMD_READ_STATUS_REG[0], [CMD_READ_STATUS_REG[1]])
        data = self.__bus.read_i2c_block_data(self.__address, REG_BASE, LEN_STATUS_REG)
        status_data = data[0] << 8 | data[1]

        result = {
            "Alert pending": self.alert_pending_status(data=status_data),
            "Heater status": self.heater_status(data=status_data),
            "RH tracking alert": self.humidity_tracking_status(data=status_data),
            "T tracking alert": self.temperature_tracking_status(data=status_data),
            "System reset detected": self.system_reset_status(data=status_data),
            "Command status": self.command_status(data=status_data),
            "Write data checksum status": self.write_data_checksum_status(data=status_data)
        }

        for key, value in result.items():
            print(f"{key:<27}: {value}")

    def get_temperature_celsius(self, data: int) -> float:
        #   Temperature conversion formula (Celsius)
        #   T[C] = -45 + (175 * (raw_temp_data / (2^16 - 1)))
        return round(-45 + (175 * (data / ((2**16) - 1))), 2)

    def get_temperature_fahrenheit(self, data: int) -> float:
        #   Temperature conversion formula (Fahrenheit)
        #   T[F] = -49 + (315 * (raw_temp_data / (2^16 - 1)))
        return round(-49 + (315 * (data / ((2**16) - 1))), 2)

    def get_relative_humidity(self, data: int) -> float:
        #   Relative humidity conversion formula
        #   RH = 100 * (raw_humidity_data / (2^16 - 1))
        return round(100 * (data / ((2**16) - 1)), 2)

    def get_sensor_info(self) -> SensorInfo:
        # TODO
        pass

    def get_measurement(self, as_dict: bool = False) -> SensorData:
        if (time() - self.__tracker < 1):
            sleep(1)

        self.__bus.write_i2c_block_data(self.__address, self.__clock_stretching, [self.__repeatability])
        sleep(0.05)

        # Read 6 bytes of raw data
        data = self.__bus.read_i2c_block_data(self.__address, REG_BASE, LEN_TEMP_HUMI_DATA)

        # Raw temperature data
        temp_data = data[0] << 8 | data[1]

        # Raw humidity data
        humi_data = data[3] << 8 | data[4]

        self.__tracker = time()

        measured = SensorData([
            Measurement("temperature", "C", self.get_temperature_celsius(temp_data)),
            Measurement("temperature", "F", self.get_temperature_fahrenheit(temp_data)),
            Measurement("relative humidity", "%", self.get_relative_humidity(humi_data))
        ])

        if as_dict == True:
            return asdict(measured)

        return measured
