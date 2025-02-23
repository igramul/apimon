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

