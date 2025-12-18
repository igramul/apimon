from typing import List, Tuple, Optional

from .models.color import Color


class ConsolePixel(List[Tuple[int, int, int]]):
    # NeoPixel Duck Typing Class for the console
    # https://realpython.com/duck-typing-python/

    _instance_counter = 0  # Klassenvariable für den Enumerator

    def __init__(self, pin: Optional[int], n: int, name: str):
        super().__init__([Color.black.tuple] * n)
        self.pin = pin
        self.name = name
        # Jede Instanz bekommt ihre eigene Nummer
        self._instance_id = ConsolePixel._instance_counter
        ConsolePixel._instance_counter += 1

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
        # Jede Instanz nutzt ihre eigene Zeile basierend auf der instance_id
        # Bewege den Cursor zur richtigen Zeile
        if self._instance_id > 0:
            print(f'\033[{self._instance_id}B', end='')  # Bewege Cursor nach unten
        print(f'\r\033[0m|{self.name}:{self._led_strip}\033[0m|', end='')
        if self._instance_id > 0:
            print(f'\033[{self._instance_id}A', end='')  # Bewege Cursor zurück nach oben
        print(flush=True)

    def _clear(self):
        # Clear the line after printing to avoid overlap
        # Bewege den Cursor zur richtigen Zeile
        if self._instance_id > 0:
            print(f'\033[{self._instance_id}B', end='')  # Bewege Cursor nach unten
        print('\r' + ' ' * (len(self.name) + self.n + 4) + '\r', end='')  # Clear the line
        if self._instance_id > 0:
            print(f'\033[{self._instance_id}A', end='')  # Bewege Cursor zurück nach oben

    @property
    def _led_strip(self):
        # Generate a line with 40 random colors
        return ''.join([Color.from_tuple(color_tuple).char for color_tuple in self])

    @property
    def n(self):
        return len(self)
