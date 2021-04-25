from time import sleep
from smbus2 import SMBus


CMD_READ_STATUS_REG = [0xF3, 0x2D]
CMD_CLEAR_STATUS_REG = [0x30, 0x41]

REG_BASE = 0x00

LEN_STATUS_REG = 3
LEN_TEMP_HUMI_DATA = 6

CLK_STRETCHING = {
    "ENABLED": 0x2C,
    "DISABLED": 0x24
}

REPEATABILITY = {
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

    def __init__(self, bus_obj:SMBus, address:int):
        self.__bus = bus_obj
        self.__address = address
        self.__clock_stretching = CLK_STRETCHING["DISABLED"]
        self.__repeatability = REPEATABILITY["DISABLED"]["HIGH"]
        self.read_status_register()

    def crc_check(self, data:list, checksum:int) -> bool:
        return self.crc_calc(data) == checksum
    
    def crc_calc(self, data:list) -> int:
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
    
    def alert_pending_status(self, data:int, verbose:bool) -> str:
        status = (data & 0b1000000000000000) >> 15

        if verbose:
            return "At least one pending alert" if status else "No pending alerts"
        else:
            return str(status)

    def heater_status(self, data:int, verbose:bool) -> str:
        status = (data & 0b0010000000000000) >> 13

        if verbose:
            return "Heater ON" if status else "Heater OFF"
        else:
            return str(status)

    def humidity_tracking_status(self, data:int, verbose:bool) -> str:
        status = (data & 0b0000100000000000) >> 11

        if verbose:
            return "Alert" if status else "No alert"
        else:
            return str(status)

    def temperature_tracking_status(self, data:int, verbose:bool) -> str:
        status = (data & 0b0000010000000000) >> 10

        if verbose:
            return "Alert" if status else "No alert"
        else:
            return str(status)

    def system_reset_status(self, data:int, verbose:bool) -> str:
        status = (data & 0b0000000000010000) >> 4

        if verbose:
            return "Reset detected" if status else "No reset detected"
        else:
            return str(status)

    def command_status(self, data:int, verbose:bool) -> str:
        status = (data & 0b0000000000000010) >> 1

        if verbose:
            return "Last command not processed" if status else "Last command executed successfully"
        else:
            return str(status)  

    def write_data_checksum_status(self, data:int, verbose:bool) -> str:
        status = data & 0b0000000000000001

        if verbose:
            return "Failed" if status else "Correct"
        else:
            return str(status)  
        
    def read_status_register(self, verbose:bool=True):
        self.__bus.write_i2c_block_data(self.__address, CMD_READ_STATUS_REG[0], [CMD_READ_STATUS_REG[1]])
        data = self.__bus.read_i2c_block_data(self.__address, REG_BASE, LEN_STATUS_REG)
        status_data = data[0] << 8 | data[1]

        result = {
            "Alert_pending": self.alert_pending_status(data=status_data, verbose=verbose),
            "Heater_status": self.heater_status(data=status_data, verbose=verbose),
            "RH_tracking_alert": self.humidity_tracking_status(data=status_data, verbose=verbose),
            "T_tracking_alert": self.temperature_tracking_status(data=status_data, verbose=verbose),
            "System_reset_detected": self.system_reset_status(data=status_data, verbose=verbose),
            "Command_status": self.command_status(data=status_data, verbose=verbose),
            "Write_data_checksum_status": self.write_data_checksum_status(data=status_data, verbose=verbose)
        }

        for key, value in result.items():
            print(f"{key.replace('_', ' '):<27}: {value}")

    def get_temperature_in_celsius(self, data:int) -> float:
        #   Temperature conversion formula (Celsius)
        #   T[C] = -45 + (175 * (raw_temp_data / (2^16 - 1)))
        return round(-45 + (175 * (data / ((2**16) - 1))), 2)    

    def get_temperature_in_fahrenheit(self, data:int) -> float:
        #   Temperature conversion formula (Fahrenheit)
        #   T[F] = -49 + (315 * (raw_temp_data / (2^16 - 1)))
        return round(-49 + (315 * (data / ((2**16) - 1))), 2)

    def get_relative_humidity(self, data:int) -> float:
        #   Relative humidity conversion formula
        #   RH = 100 * (raw_humidity_data / (2^16 - 1))
        return round(100 * (data/ ((2**16) - 1)), 2)

    def get_measurement(self) -> dict:

        sleep(0.05)
        self.__bus.write_i2c_block_data(self.__address, self.__clock_stretching, [self.__repeatability])         
        sleep(0.05)
        
        # Read 6 bytes of raw data
        data = self.__bus.read_i2c_block_data(self.__address, REG_BASE, LEN_TEMP_HUMI_DATA)

        # Raw temperature data
        temp_data = data[0] << 8 | data[1]

        # Raw humidity data
        humi_data = data[3] << 8 | data[4]

        sleep(0.05)

        return {
            "temp_celsius": self.get_temperature_in_celsius(temp_data),
            "temp_celsius_unit": "C",
            "temp_fahrenheit": self.get_temperature_in_fahrenheit(temp_data),
            "temp_fahrenheit_unit": "F",
            "relative_humidity": self.get_relative_humidity(humi_data),
            "relative_humidity_unit": "%"
        }


class SHT31(SHT3X):

    def __init__(self, bus_obj:SMBus, address:int=68):
        self.bus = bus_obj
        self.address = address # 0x44
        super().__init__(self.bus, self.address)


class SHT35(SHT3X):

    def __init__(self, bus_obj:SMBus, address:int=69):
        self.bus = bus_obj
        self.address = address # 0x45
        super().__init__(self.bus, self.address)



# Uncomment for test

# import sys
# from datetime import datetime


# bus = SMBus(1)
# sen = SHT31(bus_obj=bus)


# while True:
#     try:
#         print(datetime.now(), sen.get_measurement())
#         sleep(3)

#     except KeyboardInterrupt:
#         sys.exit(1)
