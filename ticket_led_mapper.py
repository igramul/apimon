import math
from collections import OrderedDict

import colors


class TicketLedMapper(object):

    def __init__(self, led_count: int) -> None:

        self._led_count = led_count
        self._leds = None
        self._overflow = False
        self._init_leds()

    def _init_leds(self):
        self._leds = [colors.black] * self._led_count

    def set_ticket(self, tickets: OrderedDict[str, int]) -> None:

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
            leds += [colors.black] * (self._led_count - tickets_count)

        self._leds = leds

    @property
    def leds(self) -> list:
        return self._leds

    @property
    def overflow(self) -> bool:
        return self._overflow
