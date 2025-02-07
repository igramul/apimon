from collections import OrderedDict
import pytest

from app.models.color import Color

from app.ticket_led_mapper import TicketLedMapper

LED_COUNT = 10

@pytest.fixture
def default_mapper():
    return TicketLedMapper(led_count=LED_COUNT)


def test_init_leds(default_mapper):
    # Test if LEDs are initialized to black and no overflow occurs
    assert len(default_mapper.leds) == LED_COUNT
    assert default_mapper.leds == [Color.black] * LED_COUNT
    assert default_mapper.overflow is False


def test_set_ticket_exact_fit_order(default_mapper):
    # Test ticket distribution where the total matches the LED count
    tickets = OrderedDict([(Color.red, 4), (Color.green, 3), (Color.blue, 3)])
    default_mapper.set_ticket(tickets)
    expected_leds = [Color.blue] * 3 + [Color.green] * 3 + [Color.red] * 4
    assert len(default_mapper.leds) == LED_COUNT
    assert default_mapper.leds == expected_leds
    assert default_mapper.overflow is False


def test_set_ticket_overflow_with_order(default_mapper):
    # Test ticket distribution with overflow
    tickets = OrderedDict([(Color.red, 5), (Color.green, 5), (Color.blue, 5)])
    default_mapper.set_ticket(tickets)
    expected_leds = [Color.blue] * 4 + [Color.green] * 3 + [Color.red] * 3
    assert len(default_mapper.leds) == LED_COUNT
    assert default_mapper.leds == expected_leds
    assert default_mapper.overflow is True


def test_set_ticket_single_color_with_order(default_mapper):
    # Test ticket distribution with only one color
    tickets = OrderedDict([(Color.green, 7)])
    default_mapper.set_ticket(tickets)
    expected_leds = [Color.green] * 7 + [Color.black] * 3
    assert len(default_mapper.leds) == LED_COUNT
    assert default_mapper.leds == expected_leds
    assert default_mapper.overflow is False


def test_set_ticket_no_tickets(default_mapper):
    # Test when no tickets are provided
    tickets = OrderedDict()
    default_mapper.set_ticket(tickets)
    assert len(default_mapper.leds) == LED_COUNT
    assert default_mapper.leds == [Color.black] * 10
    assert default_mapper.overflow is False


def test_set_ticket_large_overflow_with_order(default_mapper):
    # Test large overflow scenario
    tickets = OrderedDict([(Color.red, 50), (Color.green, 30), (Color.blue, 20)])
    default_mapper.set_ticket(tickets)
    expected_leds = [Color.blue] * 2 + [Color.green] * 3 + [Color.red] * 5
    assert len(default_mapper.leds) == LED_COUNT
    assert default_mapper.leds == expected_leds
    assert default_mapper.overflow is True


def test_set_ticket_partial_distribution_and_order(default_mapper):
    # Test uneven ticket distribution
    tickets = OrderedDict([(Color.red, 6), (Color.green, 2), (Color.blue, 2)])
    default_mapper.set_ticket(tickets)
    expected_leds = [Color.blue] * 2 + [Color.green] * 2 + [Color.red] * 6
    assert len(default_mapper.leds) == LED_COUNT
    assert default_mapper.leds == expected_leds
    assert default_mapper.overflow is False


def test_set_ticket_rebalances_colors_with_order(default_mapper):
    # Test redistribution in case of overflow with rebalancing
    tickets = OrderedDict([(Color.red, 8), (Color.green, 6), (Color.blue, 6)])
    default_mapper.set_ticket(tickets)
    expected_leds = [Color.blue] * 3 + [Color.green] * 3 + [Color.red] * 4
    assert len(default_mapper.leds) == LED_COUNT
    assert default_mapper.leds == expected_leds
    assert default_mapper.overflow is True


def test_set_ticket_with_min_colors_with_order(default_mapper):
    # Test redistribution in case of overflow  min number of one color
    tickets = OrderedDict([(Color.red, 200), (Color.green, 1), (Color.blue, 100)])
    default_mapper.set_ticket(tickets)
    expected_leds = [Color.blue] * 4 + [Color.green] * 1 + [Color.red] * 5
    assert len(default_mapper.leds) == LED_COUNT
    assert default_mapper.leds == expected_leds
    assert default_mapper.overflow is True
