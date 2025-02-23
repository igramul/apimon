from typing import List
from threading import Lock
import time

import board
from neopixel import NeoPixel

from color import Color
from status import STATUS


class NeoPixelController(object):

    PULSING_PERIOD = 1

    def __init__(self, led_count: int) -> None:
        self._lock: Lock = Lock()
        self._pixels: NeoPixel = NeoPixel(board.D18, led_count)
        self._pixels.fill(Color.black.tuple)
        self._pixels.show()
        self._pixel_array = [Color.black.tuple] * led_count
        self._led_array: List[Color] = [Color.black] * led_count
        self._status: STATUS = STATUS.INIT
        self._connection_error: bool = False
        self._error: bool = False
        self._overflow: bool = False
        self._init()
        self._status = STATUS.WORKING

    def __del__(self) -> None:
        self._pixels.fill(Color.black.tuple)
        self._pixels.show()

    def _init(self) -> None:
        with self._lock:
            for _ in range(2):
                for i in range(self._pixels.n):
                    self._led_array[i] = Color.random - Color.grey(50)
                self._update()
                time.sleep(0.1)
            for i in range(self._pixels.n - 1):
                self._led_array = [Color.black] * self._pixels.n
                self._led_array[i] = Color.white
                self._update()
                time.sleep(0.5 / self._pixels.n)
            for i in reversed(range(self._pixels.n)):
                self._led_array = [Color.black] * self._pixels.n
                self._led_array[i] = Color.white
                self._update()
                time.sleep(0.5 / self._pixels.n)
            self._led_array = [Color.black] * self._pixels.n
            self._update()

    def set_leds(self, leds: List[Color]) -> None:
        with self._lock:
            self._led_array = leds

    def set_connection_error(self, status) -> None:
        with self._lock:
            self._connection_error = status

    def set_error(self, status) -> None:
        with self._lock:
            self._error = status

    def update(self) -> None:
        if self._status == STATUS.INIT:
            return
        with self._lock:
            self._update()

    def _update(self) -> None:
        # update LED array to pixel array
        for index, color in enumerate(self._led_array):
            if self._pixel_array[index] != color.tuple:
                self._pixel_array[index] = color.tuple
                self._pixels[index] = color.tuple

        # update status
        if self._error:
            self._status = STATUS.ERROR
        elif self._connection_error:
            self._status = STATUS.CONNECTION_ERROR
        else:
            self._status = STATUS.WORKING

        # update status LED (index 0)
        cycle_time = time.time() % (2 * self.PULSING_PERIOD)
        color = Color.black
        if cycle_time > self.PULSING_PERIOD:
            if self._status == STATUS.INIT:
                color = Color.black
            elif self._status == STATUS.WORKING:
                color = Color.white
            elif self._status == STATUS.CONNECTION_ERROR:
                color = Color.orange
            elif self._status == STATUS.ERROR:
                color = Color.red
        self._pixels[0] = (color + self._led_array[0]).tuple
        self._pixels.show()

    @property
    def leds(self) -> List[Color]:
        return self._led_array

    @property
    def status(self) -> STATUS:
        return self._status