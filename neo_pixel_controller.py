import board
import neopixel
import colors

class NeoPixelController:
    def __init__(self):
        self.pixels = neopixel.NeoPixel(board.D18, 40)
        self.pixel_array = [colors.black, 10]
        self.status_color_map = {
            'Checking': colors.green,
            'Deferred': colors.blue,
            'In Progress': colors.magenta,
            'Open': colors.red
        }

    def update_pixels(self, tickets, status_list):
        index = 0
        if self.pixel_array[0] == colors.weiss:
            self.pixel_array[0] = colors.black
        else:
            self.pixel_array[0] = colors.weiss
        self.pixels[index] = self.pixel_array[0]

        self.pixel_array[1] = self.pixel_array[1] + 1
        if self.pixel_array[1] < 10:
            self.pixels.show()
            return
        self.pixel_array[1] = 0

        index += 1
        for status in reversed(status_list):
            count = tickets.get(status)
            if not count:
                continue
            color = self.status_color_map.get(status)
            for i in range(count):
                self.pixels[index + i] = color
            index += count
        for i in range(index, self.pixels.n):
            self.pixels[i] = colors.black
        self.pixels.show()
