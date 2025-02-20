import logging
import atexit

from flask import Flask, jsonify
from flask_apscheduler import APScheduler
from dotenv import load_dotenv

from jira_ticket_fetcher import JiraTicketFetcher
from ticket_led_mapper import TicketLedMapper

try:
    from neopixel_controller import NeoPixelController
except NotImplementedError:
    from nopixel_controller import NoPixelController as NeoPixelController

import version

LED_COUNT = 40

# Load environment variables from .env file
load_dotenv()

ticket_fetcher = JiraTicketFetcher()
ticket_led_mapper = TicketLedMapper(LED_COUNT)
neopixel_controller = NeoPixelController(LED_COUNT)

# set configuration values
class Config:
    SCHEDULER_API_ENABLED = True

logging.basicConfig(level=logging.INFO)
app = Flask(__name__)
app.config.from_object(Config())

# initialize scheduler
scheduler = APScheduler()
scheduler.init_app(app)
scheduler.start()

logging.getLogger('apscheduler.executors.default').setLevel(logging.WARNING)

@app.route('/')
def get_root():
    return jsonify({
        'name': 'apimon',
        'version': version.version,
        'tickets': ticket_fetcher.tickets,
        'pixels': neopixel_controller.pixels,
    })

@scheduler.task('cron', id='do_job_update_tickets', minute='*/5')
def job_update_tickets():
    ticket_fetcher.update_tickets()

@scheduler.task('interval', id='do_job_update_pixels', seconds=0.1)
def job_update_pixels():
    colors = ticket_fetcher.colors
    ticket_led_mapper.set_ticket(colors)
    leds = ticket_led_mapper.leds
    neopixel_controller.update_pixels(leds)

def cleanup():
    del neopixel_controller

atexit.register(cleanup)

if __name__ == '__main__':
    app.run()
