import json

from .JiraTicketLedStripe import JiraTicketLedStripe


class JiraTicketLedStripeList(list):

    def __init__(self):
        super().__init__()
        self._jira_tickets_led_stripes = list()
        with open('config.json', 'r') as f:
            config = json.load(f)
            for led_stripe in config:
                self.append(
                    JiraTicketLedStripe(
                        name=led_stripe.get('name'),
                        jira_filter=led_stripe.get('jira_filter'),
                        gpio_pin=led_stripe.get('gpio_pin'),
                        led_count=led_stripe.get('led_count'),
                        offset=led_stripe.get('offset')
                    )
                )

    def get_info_dict(self):
        return [_.get_info_dict() for _ in self]

    def clear(self):
        [_.clear() for _ in self]

    def update_tickets(self):
        [_.update_tickets() for _ in self]

    def update_pixels(self):
        [_.update_pixels() for _ in self]
