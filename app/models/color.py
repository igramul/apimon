from typing import Tuple
import random


class classproperty(property):
    def __get__(self, owner_self, owner_cls):
        return self.fget(owner_cls)


class Color(object):
    def __init__(self, r:int, g:int, b:int):
        self.r = min(r, 255)
        self.g = min(g, 255)
        self.b = min(b, 255)

    @classmethod
    def from_hex(cls, hex:int) -> 'Color':
        return cls(hex >> 16, (hex >> 8) & 0xFF, hex & 0xFF)

    @classmethod
    def from_rgb(cls, r:int, g:int, b:int) -> 'Color':
        return cls(r, g, b)

    @classmethod
    def from_tuple(cls, color_tuple: Tuple[int, int, int]) -> 'Color':
        return cls(*color_tuple)

    @classproperty
    def random(cls) -> 'Color':
        return cls.from_rgb(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))

    @classproperty
    def white(cls) -> 'Color':
        return cls.from_rgb(255, 255, 255)

    @classproperty
    def black(cls) -> 'Color':
        return cls.from_rgb(0, 0, 0)

    @classproperty
    def blue(cls) -> 'Color':
        return cls.from_rgb(0, 0, 255)

    @classproperty
    def red(cls) -> 'Color':
        return cls.from_rgb(255, 0, 0)

    @classproperty
    def green(cls) -> 'Color':
        return cls.from_rgb(0, 255, 0)

    @classproperty
    def yellow(cls) -> 'Color':
        return cls.from_rgb(255, 255, 0)

    @classproperty
    def magenta(cls) -> 'Color':
        return cls.from_rgb(255, 0, 255)

    @classproperty
    def cyan(cls) -> 'Color':
        return cls.from_rgb(0, 255, 255)

    @classproperty
    def orange(cls) -> 'Color':
        return cls.from_rgb(255, 128, 0)

    @classmethod
    def grey(cls, percent) -> 'Color':
        return cls.from_rgb(int(percent * 255 / 100), int(percent * 255 / 100), int(percent * 255 / 100))

    def adjust_brightness(self, brightness: int) -> 'Color':
        # Ensure that the value is within the valid range
        if not (0 <= brightness <= 255):
            raise ValueError(f'The brightness value must be between 0 and 255. Given value was {brightness}.')

        # Calculate the new color values based on the brightness
        new_r = min(int((brightness / 255) * self.r), 255)
        new_g = min(int((brightness / 255) * self.g), 255)
        new_b = min(int((brightness / 255) * self.b), 255)

        return Color(new_r, new_g, new_b)

    def __add__(self, other: 'Color') -> 'Color':
        return Color(
            min(self.r + other.r, 255),
            min(self.g + other.g, 255),
            min(self.b + other.b, 255)
        )

    def __sub__(self, other: 'Color') -> 'Color':
        return Color(
            max(self.r - other.r, 0),
            max(self.g - other.g, 0),
            max(self.b - other.b, 0)
        )

    def __eq__(self, other: 'Color') -> bool:
        return self.r == other.r and self.g == other.g and self.b == other.b

    def __hash__(self) -> int:
        return hash((self.r, self.g, self.b))

    @property
    def hex(self) -> int:
        return (self.r << 16) + (self.g << 8) + self.b

    @property
    def tuple(self) -> Tuple[int, int, int]:
        return self.r, self.g, self.b

    @property
    def tuple_str(self) -> str:
        return f'({self.r}, {self.g}, {self.b})'

    @property
    def char(self) -> str:
        return f'\033[38;2;{self.r};{self.g};{self.b}m■'
