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
    tickets = OrderedDict([('Open', {'color': Color.red.tuple_str, 'count': 4, 'overdue': 0}),
                           ('In Progress', {'color': Color.green.tuple_str, 'count': 3, 'overdue': 0}),
                           ('Deferred', {'color': Color.blue.tuple_str, 'count': 3, 'overdue': 0})])
    default_mapper.set_ticket(tickets)
    expected_leds = [Color.blue] * 3 + [Color.green] * 3 + [Color.red] * 4
    assert len(default_mapper.leds) == LED_COUNT
    assert default_mapper.leds == expected_leds
    assert default_mapper.overflow is False


def test_set_ticket_overflow_with_order(default_mapper):
    # Test ticket distribution with overflow
    tickets = OrderedDict([('Open', {'color': Color.red.tuple_str, 'count': 5, 'overdue': 0}),
                           ('In Progress', {'color': Color.green.tuple_str, 'count': 5, 'overdue': 0}),
                           ('Deferred', {'color': Color.blue.tuple_str, 'count': 5, 'overdue': 0})])
    default_mapper.set_ticket(tickets)
    expected_leds = [Color.blue] * 4 + [Color.green] * 3 + [Color.red] * 3
    assert len(default_mapper.leds) == LED_COUNT
    assert default_mapper.leds == expected_leds
    assert default_mapper.overflow is True


def test_set_ticket_single_color_with_order(default_mapper):
    # Test ticket distribution with only one color
    tickets = OrderedDict([('Checking', {'color': Color.green.tuple_str, 'count': 7, 'overdue': 0})])
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
    tickets = OrderedDict([('Open', {'color': Color.red.tuple_str, 'count': 50, 'overdue': 0}),
                           ('In Progress', {'color': Color.green.tuple_str, 'count': 30, 'overdue': 0}),
                           ('Deferred', {'color': Color.blue.tuple_str, 'count': 20, 'overdue': 0})])
    default_mapper.set_ticket(tickets)
    expected_leds = [Color.blue] * 2 + [Color.green] * 3 + [Color.red] * 5
    assert len(default_mapper.leds) == LED_COUNT
    assert default_mapper.leds == expected_leds
    assert default_mapper.overflow is True


def test_set_ticket_partial_distribution_and_order(default_mapper):
    # Test uneven ticket distribution
    tickets = OrderedDict([('Open', {'color': Color.red.tuple_str, 'count': 6, 'overdue': 0}),
                           ('In Progress', {'color': Color.green.tuple_str, 'count': 2, 'overdue': 0}),
                           ('Deferred', {'color': Color.blue.tuple_str, 'count': 2, 'overdue': 0})])
    default_mapper.set_ticket(tickets)
    expected_leds = [Color.blue] * 2 + [Color.green] * 2 + [Color.red] * 6
    assert len(default_mapper.leds) == LED_COUNT
    assert default_mapper.leds == expected_leds
    assert default_mapper.overflow is False


def test_set_ticket_rebalances_colors_with_order(default_mapper):
    # Test redistribution in case of overflow with rebalancing
    tickets = OrderedDict([('Open', {'color': Color.red.tuple_str, 'count': 8, 'overdue': 0}),
                           ('In Progress', {'color': Color.green.tuple_str, 'count': 6, 'overdue': 0}),
                           ('Deferred', {'color': Color.blue.tuple_str, 'count': 6, 'overdue': 0})])
    default_mapper.set_ticket(tickets)
    expected_leds = [Color.blue] * 3 + [Color.green] * 3 + [Color.red] * 4
    assert len(default_mapper.leds) == LED_COUNT
    assert default_mapper.leds == expected_leds
    assert default_mapper.overflow is True


def test_set_ticket_with_min_colors_with_order(default_mapper):
    # Test redistribution in case of overflow  min number of one color
    tickets = OrderedDict([('Open', {'color': Color.red.tuple_str, 'count': 200, 'overdue': 0}),
                           ('In Progress', {'color': Color.green.tuple_str, 'count': 1, 'overdue': 0}),
                           ('Deferred', {'color': Color.blue.tuple_str, 'count': 100, 'overdue': 0})])
    default_mapper.set_ticket(tickets)
    expected_leds = [Color.blue] * 4 + [Color.green] * 1 + [Color.red] * 5
    assert len(default_mapper.leds) == LED_COUNT
    assert default_mapper.leds == expected_leds
    assert default_mapper.overflow is True
