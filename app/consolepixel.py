from typing import List, Tuple

from .models.color import Color


class ConsolePixel(List[Tuple[int, int, int]]):
    # NeoPixel Duck Typing Class for the console
    # https://realpython.com/duck-typing-python/

    def __init__(self, pin: None, n: int, name: str):
        super().__init__([Color.black.tuple] * n)
        self.pin = pin
        self.name = name

    def init(self):
        self._print()

    def fill(self, color):
        for i in range(self.n):
            self[i] = color

    def show(self):
        self._clear()
        self._print()

    def _print(self):
        # Print the side border and the LED strip with white borders
        print(f'\r\033[0m|{self.name}:{self._led_strip}\033[0m|', end='')

    def _clear(self):
        # Clear the line after printing to avoid overlap
        print('\r' + ' ' * (len(self.name) + self.n + 2) + '\r', end='')  # Clear the line (42 spaces for "|<40 LEDs>|")

    @property
    def _led_strip(self):
        # Generate a line with 40 random colors
        return ''.join([Color.from_tuple(color_tuple).char for color_tuple in self])

    @property
    def n(self):
        return len(self)
