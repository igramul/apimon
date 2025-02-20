from collections import OrderedDict
import pytest

import colors

from ticket_led_mapper import TicketLedMapper

LED_COUNT = 10

@pytest.fixture
def default_mapper():
    return TicketLedMapper(led_count=LED_COUNT)


def test_init_leds(default_mapper):
    # Test if LEDs are initialized to black and no overflow occurs
    assert len(default_mapper.leds) == LED_COUNT
    assert default_mapper.leds == [colors.black] * LED_COUNT
    assert default_mapper.overflow is False


def test_set_ticket_exact_fit_order(default_mapper):
    # Test ticket distribution where the total matches the LED count
    tickets = OrderedDict([(colors.red, 4), (colors.green, 3), (colors.blue, 3)])
    default_mapper.set_ticket(tickets)
    expected_leds = [colors.blue] * 3 + [colors.green] * 3 + [colors.red] * 4
    assert len(default_mapper.leds) == LED_COUNT
    assert default_mapper.leds == expected_leds
    assert default_mapper.overflow is False


def test_set_ticket_overflow_with_order(default_mapper):
    # Test ticket distribution with overflow
    tickets = OrderedDict([(colors.red, 5), (colors.green, 5), (colors.blue, 5)])
    default_mapper.set_ticket(tickets)
    expected_leds = [colors.blue] * 4 + [colors.green] * 3 + [colors.red] * 3
    assert len(default_mapper.leds) == LED_COUNT
    assert default_mapper.leds == expected_leds
    assert default_mapper.overflow is True


def test_set_ticket_single_color_with_order(default_mapper):
    # Test ticket distribution with only one color
    tickets = OrderedDict([(colors.green, 7)])
    default_mapper.set_ticket(tickets)
    expected_leds = [colors.green] * 7 + [colors.black] * 3
    assert len(default_mapper.leds) == LED_COUNT
    assert default_mapper.leds == expected_leds
    assert default_mapper.overflow is False


def test_set_ticket_no_tickets(default_mapper):
    # Test when no tickets are provided
    tickets = OrderedDict()
    default_mapper.set_ticket(tickets)
    assert len(default_mapper.leds) == LED_COUNT
    assert default_mapper.leds == [colors.black] * 10
    assert default_mapper.overflow is False


def test_set_ticket_large_overflow_with_order(default_mapper):
    # Test large overflow scenario
    tickets = OrderedDict([(colors.red, 50), (colors.green, 30), (colors.blue, 20)])
    default_mapper.set_ticket(tickets)
    expected_leds = [colors.blue] * 2 + [colors.green] * 3 + [colors.red] * 5
    assert len(default_mapper.leds) == LED_COUNT
    assert default_mapper.leds == expected_leds
    assert default_mapper.overflow is True


def test_set_ticket_partial_distribution_and_order(default_mapper):
    # Test uneven ticket distribution
    tickets = OrderedDict([(colors.red, 6), (colors.green, 2), (colors.blue, 2)])
    default_mapper.set_ticket(tickets)
    expected_leds = [colors.blue] * 2 + [colors.green] * 2 + [colors.red] * 6
    assert len(default_mapper.leds) == LED_COUNT
    assert default_mapper.leds == expected_leds
    assert default_mapper.overflow is False


def test_set_ticket_rebalances_colors_with_order(default_mapper):
    # Test redistribution in case of overflow with rebalancing
    tickets = OrderedDict([(colors.red, 8), (colors.green, 6), (colors.blue, 6)])
    default_mapper.set_ticket(tickets)
    expected_leds = [colors.blue] * 3 + [colors.green] * 3 + [colors.red] * 4
    assert len(default_mapper.leds) == LED_COUNT
    assert default_mapper.leds == expected_leds
    assert default_mapper.overflow is True


def test_set_ticket_with_min_colors_with_order(default_mapper):
    # Test redistribution in case of overflow  min number of one color
    tickets = OrderedDict([(colors.red, 200), (colors.green, 1), (colors.blue, 100)])
    default_mapper.set_ticket(tickets)
    expected_leds = [colors.blue] * 4 + [colors.green] * 1 + [colors.red] * 5
    assert len(default_mapper.leds) == LED_COUNT
    assert default_mapper.leds == expected_leds
    assert default_mapper.overflow is True
