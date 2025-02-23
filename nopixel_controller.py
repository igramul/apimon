from typing import List

from color import Color

from status import STATUS


class NoPixelController(object):

    def __init__(self, led_count: int) -> None:
        self._led_array: List[Color] = [Color.black] * led_count
        self._status: STATUS = STATUS.WORKING
        self._connection_error: bool = False
        self._error: bool = False
        self._overflow: bool = False

    def set_leds(self, leds: list) -> None:
        self._led_array = leds

    def set_connection_error(self, status) -> None:
        self._connection_error = status

    def set_error(self, status) -> None:
        self._error = status

    def update(self) -> None:
        # update status
        if self._error:
            self._status = STATUS.ERROR
        elif self._connection_error:
            self._status = STATUS.CONNECTION_ERROR
        else:
            self._status = STATUS.WORKING

    @property
    def leds(self) -> List[Color]:
        return self._led_array

    @property
    def status(self) -> STATUS:
        return self._status
