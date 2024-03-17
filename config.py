from dataclasses import dataclass

import snap7


class Status:
    RANGE = (0, 2)

    I_LEVEL = 0
    X_PUMP_RUNNING = 2
    X_VALVE_OPEN = 2.1
    X_FAULTED = 2.2
    X_LOW_LEVEL = 2.3


class Supply:
    STATUS = Status()


class Equipment:
    SUPPLY = Supply()


class DataBlock:
    EQUIPMENT = 4


class StatusDataBlock:
    DB_NUMBER = 4

    class BytesMapping:
        IlEVEL = 0
        PUMP_RUNNING = 2
        VALVE_OPEN = 2
        FAULTED = 2
        LOW_LEVEL = 2

    def __init__(self, connection: snap7.client.Client) -> None:
        self._plc = connection

    def _get_current_byte(self, byte: int, offset: int = 1) -> bytearray:
        """
        Get current value of a given byte
        """
        return self._plc.db_read(self.DB_NUMBER, start=byte, size=offset)

    def _set_current_byte(self, byte: int, data: bytearray) -> bytearray:
        """
        Set current value of a given byte
        """
        return self._plc.db_write(self.DB_NUMBER, start=byte, data=data)

    @property
    def level(self) -> int:
        offset = 2
        reading = self._get_current_byte(byte=self.BytesMapping.IlEVEL, offset=offset)
        return int.from_bytes(reading)

    @level.setter
    def level(self, level: int) -> None:
        closest_bytes = level.bit_length() + 7
        data = level.to_bytes(closest_bytes // 8)
        self._set_current_byte(byte=self.BytesMapping.IlEVEL, data=data)