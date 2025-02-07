from typing import List
import math
from collections import OrderedDict

from .models.color import Color


class TicketLedMapper(object):

    def __init__(self, led_count: int) -> None:
        self._led_count: int = led_count
        self._leds: List[Color] = [Color.black] * self._led_count
        self._overflow: bool = False

    def set_ticket(self, tickets: OrderedDict[Color, int]) -> None:

        tickets_count = sum(tickets.values())
        if tickets_count > self._led_count:
            self._overflow = True
            # scale tickets to led_count
            for color in tickets.keys():
                tickets[color] = math.ceil(tickets.get(color) * self._led_count / tickets_count)
            # reduce the color with the most of the leds by one as long as we have more than led_count
            while sum(tickets.values()) > self._led_count:
                color_with_most_tickets = max(tickets, key=lambda k: tickets[k])
                tickets[color_with_most_tickets] -= 1
        else:
            self._overflow = False

        leds = []
        for color in reversed(tickets.keys()):
            count = tickets.get(color)
            leds += [color] * count

        if not self._overflow:
            leds += [Color.black] * (self._led_count - tickets_count)

        self._leds = leds

    @property
    def leds(self) -> List[Color]:
        return self._leds

    @property
    def overflow(self) -> bool:
        return self._overflow
