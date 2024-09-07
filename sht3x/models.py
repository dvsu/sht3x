from dataclasses import dataclass
from typing import Optional


@dataclass
class SensorInfo:
    maker: str
    model: Optional[str]
    serial: Optional[str]
    version: Optional[str]


@dataclass
class Measurement:
    name: str
    unit: str
    value: float
    timestamp: str


@dataclass
class SensorData:
    sensor: SensorInfo
    measurements: list[Measurement]
