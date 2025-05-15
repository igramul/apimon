from rpi_ws281x import PixelStrip, Color as rpi_color

# LED strip configuration:
# LED_COUNT = 16        # Number of LED pixels.
# LED_PIN = 18          # GPIO pin connected to the pixels (18 uses PWM!).
# LED_PIN = 10          # GPIO pin connected to the pixels (10 uses SPI /dev/spidev0.0).
LED_FREQ_HZ = 800000  # LED signal frequency in hertz (usually 800khz)
LED_DMA = 10          # DMA channel to use for generating signal (try 10)
LED_BRIGHTNESS = 255  # Set to 0 for darkest and 255 for brightest
LED_INVERT = False    # True to invert the signal (when using NPN transistor level shift)
# LED_CHANNEL = 0       # set to '1' for GPIOs 13, 19, 41, 45 or 53


def get_led_channel(pin):
    if pin in [ 13, 19, 41, 45, 53]:
        return 1
    else:
        return 0


class Pixel(object):

    def __init__(self, led_pin: int, led_count: int, name: str):
        # Create NeoPixel object with appropriate configuration.
        led_channel = get_led_channel(led_pin)
        print(f'name={name}, pin={led_pin}, LED_CHANNEL={led_channel}')
        self.strip = PixelStrip(led_count, led_pin, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, led_channel)
        # Initialize the library (must be called once before other functions).
        self.strip.begin()
        self.name = name

    def fill(self, color: tuple):
        for i in range(self.strip.numPixels()):
            self.strip.setPixelColor(i, rpi_color(*color))

    def show(self):
        self.strip.show()

    @property
    def n(self) -> int:
        return self.strip.numPixels()

    def __setitem__(self, key: int, color: tuple):
        self.strip.setPixelColor(key, rpi_color(*color))
