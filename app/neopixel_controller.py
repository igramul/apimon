from typing import List
from threading import Lock
import time
import math

try:
    import board
    from neopixel import NeoPixel as Pixel
except ModuleNotFoundError:
    from .rpi_ws281x_pixel import board, Pixel
except NotImplementedError:
    from .consolepixel import none_board as board
    from .consolepixel import ConsolePixel as Pixel

from .models.color import Color, ColorEffects
from .status import STATUS


class NeoPixelController(object):

    PULSING_PERIOD = 2

    def __init__(self, led_count: int) -> None:
        self._lock: Lock = Lock()
        self._pixels: Pixel = Pixel(board.D18, led_count)
        self._pixels.fill(Color.black.tuple)
        self._pixels.show()
        self._pixel_array: List[Color] = [Color.black] * led_count
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

    def set_connection_error(self, status: bool) -> None:
        with self._lock:
            self._connection_error = status

    def set_error(self, status: bool) -> None:
        with self._lock:
            self._error = status

    def set_overflow(self, status: bool) -> None:
        with self._lock:
            self._overflow = status

    def update(self) -> None:
        if self._status == STATUS.INIT:
            return
        with self._lock:
            self._update()

    def _update(self) -> None:
        # update LED array to pixel array
        for index, status_color in enumerate(self._led_array):
            if self._pixel_array[index] != status_color:
                self._pixel_array[index] = status_color
                self._pixels[index] = status_color.tuple

        # update status
        if self._error:
            self._status = STATUS.ERROR
        elif self._connection_error:
            self._status = STATUS.CONNECTION_ERROR
        else:
            self._status = STATUS.WORKING

        # update status LED (index 0)
        if self._status == STATUS.INIT:
            status_color = Color.black
        elif self._status == STATUS.WORKING:
            status_color = Color.white
        elif self._status == STATUS.CONNECTION_ERROR:
            status_color = Color.orange
        elif self._status == STATUS.ERROR:
            status_color = Color.red
        else:
            status_color = Color.black

        cycle_time = time.time() % self.PULSING_PERIOD
        pulsing_brightness = int(math.sin(cycle_time * self.PULSING_PERIOD * math.pi / 2) * 255)
        color_status = status_color.adjust_brightness(max(pulsing_brightness, 0))
        self._pixels[0] = (color_status + self._led_array[0]).tuple

        if self._overflow:
            color_overflow = Color.white.adjust_brightness(max(pulsing_brightness, 0))
            self._pixels[-1] = (color_overflow + self._led_array[-1]).tuple

        # handle pixel effects
        pulsing_brightness_overdue = min(max(int(math.sin(cycle_time * self.PULSING_PERIOD*2 * math.pi / 2) * 128)+192, 0), 255)
        for i, pixel in enumerate(self._pixel_array):
            if pixel.effect == ColorEffects.overdue:
                self._pixels[i] = self._led_array[i].adjust_brightness(pulsing_brightness_overdue).tuple

        self._pixels.show()

    @property
    def leds(self) -> List[Color]:
        return self._led_array

    @property
    def status(self) -> STATUS:
        return self._status

    @property
    def overflow(self) -> bool:
        return self._overflow
