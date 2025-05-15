from typing import List
import math
from collections import OrderedDict

from .models.color import Color, ColorEffects


class TicketLedMapper(object):

    def __init__(self, led_count: int, name: str) -> None:
        self._led_count: int = led_count
        self.name = name
        self._leds: List[Color] = [Color.black] * self._led_count
        self._overflow: bool = False

    def set_ticket(self, tickets: OrderedDict[str, dict]) -> None:

        color_counts: OrderedDict[str, int] = OrderedDict()
        color_counts_overdue: OrderedDict[str, int] = OrderedDict()
        for item in tickets.values():
            color_counts[item.get('color')] = item.get('count')
            color_counts_overdue[item.get('color')] = item.get('overdue')

        total_count = sum(color_counts.values())
        if total_count > self._led_count:
            self._overflow = True
            # scale color count to led_count
            for color, count in color_counts.items():
                color_counts[color] = math.ceil(count * self._led_count / total_count)
            # reduce the color with the most of the leds by one as long as we have more than led_count
            while sum(color_counts.values()) > self._led_count:
                color_with_max_count = max(color_counts, key=lambda k: color_counts[k])
                color_counts[color_with_max_count] -= 1
        else:
            self._overflow = False

        leds = []
        for color_str, count in reversed(color_counts.items()):
            color = Color.from_tuple_str(color_str)
            color_overdue = Color.from_tuple_str(color_str)
            color_overdue.set_effect(ColorEffects.overdue)
            overdue_count = min(color_counts_overdue.get(color_str), count)
            color_array = [color] * (count - overdue_count) + [color_overdue] * overdue_count
            leds += color_array

        if not self._overflow:
            leds += [Color.black] * (self._led_count - total_count)

        self._leds = leds

    @property
    def leds(self) -> List[Color]:
        return self._leds

    @property
    def overflow(self) -> bool:
        return self._overflow
