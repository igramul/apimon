import logging
from enum import Enum, auto
from threading import Lock
import time

import board
import neopixel

from color import Color


class STATUS(Enum):
    INIT = auto()
    WORKING = auto()
    ERROR_NETWORK = auto()
    ERROR = auto()


class NeoPixelController(object):

    PULSING_PERIOD = 1

    def __init__(self, led_count: int):
        self._lock = Lock()
        self._pixels = neopixel.NeoPixel(board.D18, led_count)
        self._pixels.fill(Color.black.tuple)
        self._pixels.show()
        self._pixel_array = [Color.black.tuple] * led_count
        self._led_array = [Color.black] * led_count
        self._status = STATUS.INIT
        self._overflow = False
        self._init()

    def __del__(self):
        self._pixels.fill(Color.black.tuple)
        self._pixels.show()

    def _init(self):
        with self._lock:
            for _ in range(5):
                for i in range(self._pixels.n):
                    self._led_array[i] = Color.random - Color.grey50
                self._update()
                time.sleep(0.15)

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
        self._status = STATUS.WORKING

    def set_leds(self, leds: list):
        with self._lock:
            self._led_array = leds

    def update(self):
        with self._lock:
            self._update()

    def _update(self):
        # update LED array to pixel array
        for index, color in enumerate(self._led_array):
            if self._pixel_array[index] != color.tuple:
                self._pixel_array[index] = color.tuple
                self._pixels[index] = color.tuple

        # pulsing status LED (index 0)
        if self._status == STATUS.WORKING:
            cycle_time = time.time() % (2 * self.PULSING_PERIOD)
            logging.debug(f"cycle_time: {cycle_time}")
            if cycle_time < self.PULSING_PERIOD:
                color = Color.white
            else:
                color = Color.black
            self._pixels[0] = (color + self._led_array[0]).tuple

        self._pixels.show()

    @property
    def leds(self):
        return self._led_array
