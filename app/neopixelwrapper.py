from neopixel import NeoPixel


class Pin(object):

    def __init__(self, id):
        self.id = id


class Pixel(NeoPixel):

    def __init__(self, gpio_pin, led_count, name):
        pin = Pin(gpio_pin)
        super().__init__(pin, led_count)
        self.name = name
