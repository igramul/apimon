import math

import board
import neopixel

import colors

class NeoPixelController:
    def __init__(self, led_count: int):

        self.pixels = neopixel.NeoPixel(board.D18, led_count)
        self.pixels_array = [None] * led_count
        self.update_pixels([colors.black] * led_count)

    def update_pixels(self, leds: list ):

        for index, color in enumerate(leds):
            if self.pixels_array[index] != color:
                self.pixels_array[index] = color
                self.pixels[index] = color

        self.pixels.show()


