import colors


class NoPixelController:

    def __init__(self, led_count: int):

        self._pixels_array = [None] * led_count
        self.update_pixels([colors.black] * led_count)

    def update_pixels(self, leds: list ):

        for index, color in enumerate(leds):
            if self._pixels_array[index] != color:
                self._pixels_array[index] = color

    @property
    def pixels(self):
        return self._pixels_array
