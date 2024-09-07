from typing import Optional

from pydantic import BaseModel


class SensorInfo(BaseModel):
    maker: str
    model: Optional[str]
    serial: Optional[str]
    version: Optional[str]


class Measurement(BaseModel):
    name: str
    unit: str
    value: float
    datetime_utc: str
    timestamp_nanosec: int


class SensorData(BaseModel):
    sensor: SensorInfo
    measurements: list[Measurement]
