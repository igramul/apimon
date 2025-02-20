import board
import neopixel

import colors


class NeoPixelController:

    def __init__(self, led_count: int):

        self._pixels = neopixel.NeoPixel(board.D18, led_count)
        self._pixels_array = [None] * led_count
        self.update_pixels([colors.black] * led_count)

    def update_pixels(self, leds: list ):

        for index, color in enumerate(leds):
            if self._pixels_array[index] != color:
                self._pixels_array[index] = color
                self._pixels[index] = color

        self._pixels.show()

    @property
    def pixels(self):
        return self._pixels_array
