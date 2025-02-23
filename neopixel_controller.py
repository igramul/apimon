import logging
from enum import Enum, auto
from threading import Lock
import time

import board
import neopixel

from nopixel_controller import NoPixelController
import colors


class STATUS(Enum):
    INIT = auto()
    WORKING = auto()
    ERROR_NETWORK = auto()
    ERROR = auto()


class NeoPixelController(NoPixelController):

    PULSING_PERIOD = 2

    def __init__(self, led_count: int):
        super().__init__(led_count)
        self._lock = Lock()
        self._pixels = neopixel.NeoPixel(board.D18, led_count)
        self._pixels.fill(colors.black)
        self._pixels.show()
        self._pixel_array = [colors.black] * led_count
        self._led_array = [colors.black] * led_count
        self._status = STATUS.INIT
        self._overflow = False
        self._init()

    def __del__(self):
        self._pixels.fill(colors.black)
        self._pixels.show()

    def _init(self):
        with self._lock:
            for i in range(self._pixels.n):
                self._led_array[i] = colors.get_random_color()
            self._update()
            time.sleep(0.2)
            for i in range(self._pixels.n):
                self._led_array[i] = colors.get_random_color()
            self._update()
            time.sleep(0.2)

            for i in range(self._pixels.n - 1):
                self._led_array = [colors.black] * self._pixels.n
                self._led_array[i] = colors.white
                self._update()
                time.sleep(0.5 / self._pixels.n)
            for i in reversed(range(self._pixels.n)):
                self._led_array = [colors.black] * self._pixels.n
                self._led_array[i] = colors.white
                self._update()
                time.sleep(0.5 / self._pixels.n)
            self._led_array = [colors.black] * self._pixels.n
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
            if self._pixel_array[index] != color:
                self._pixel_array[index] = color
                self._pixels[index] = color

        # pulsing status LED (index 0)
        if self._status == STATUS.WORKING:
            cycle_time = time.time() % (2 * self.PULSING_PERIOD)
            logging.debug(f"cycle_time: {cycle_time}")
            if cycle_time < self.PULSING_PERIOD:
                color = colors.white
            else:
                color = colors.black
            self._pixels[0] = colors.add(color, self._pixel_array[0])

        self._pixels.show()
