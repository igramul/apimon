import colors


class NoPixelController(object):

    def __init__(self, led_count: int):
        self._led_array = [colors.black] * led_count

    def set_leds(self, leds: list):
        self._led_array = leds

    def update(self):
        pass

    @property
    def leds(self):
        return self._led_array
