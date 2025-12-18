import logging

from app.jira_ticket_fetcher import JiraTicketFetcher
from app.ticket_led_mapper import TicketLedMapper
from app.neopixel_controller import NeoPixelController


class JiraTicketLedStripe(object):

    def __init__(self, name: str, jira_filter: str, gpio_pin: int, led_count: int, offset: float):
        self.name = name
        self.jira_filter = jira_filter
        self.gpio_pin = gpio_pin
        self.led_count = led_count
        self.offset = offset

        self._ticket_fetcher = JiraTicketFetcher(name=name, jira_filter=jira_filter)
        self._ticket_led_mapper = TicketLedMapper(led_count=led_count, name=name)
        self._neopixel_controller = NeoPixelController(led_count=led_count, gpio_pin=gpio_pin, name=name, offset=offset)

    @property
    def tickets(self):
        return self._ticket_fetcher.tickets

    @property
    def leds(self):
        return self._neopixel_controller.leds

    @property
    def status(self):
        return self._neopixel_controller.status

    @property
    def overflow(self):
        return self._neopixel_controller.overflow

    def update_tickets(self):
        try:
            self._ticket_fetcher.update_tickets()
            tickets = self._ticket_fetcher.tickets
            self._ticket_led_mapper.set_ticket(tickets)
            leds = self._ticket_led_mapper.leds
            self._neopixel_controller.set_leds(leds)
            overflow = self._ticket_led_mapper.overflow
            self._neopixel_controller.set_overflow(overflow)
            self._neopixel_controller.set_error(False)
        except ConnectionError as ce:
            logging.error(f'ConnectionError beim Aktualisieren der {self.name}-Tickets: %s', ce)
            self._neopixel_controller.set_connection_error(True)
        except Exception as exc:
            logging.exception(f'Unerwarteter Fehler beim Aktualisieren der {self.name}-Tickets: %s', exc)
            self._neopixel_controller.set_error(True)
        else:
            self._neopixel_controller.set_connection_error(False)
            self._neopixel_controller.set_error(False)

    def update_pixels(self):
        try:
            self._neopixel_controller.update()
        except Exception as e:
            logging.error(f"Error updating pixels for {self.name}: {e}", exc_info=True)
            # Set error state but don't crash
            self._neopixel_controller.set_error(True)

    def clear(self):
        self._neopixel_controller.clear()

    def get_info_dict(self):
        return {
            self.name: {
                'tickets': self.tickets,
                'leds': [str(color) for color in self.leds],
                'status': self.status.name,
                'overflow': self.overflow
            }
        }
