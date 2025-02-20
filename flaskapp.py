import logging
import atexit

from flask import Flask, jsonify
from flask_apscheduler import APScheduler
from dotenv import load_dotenv

from jira_ticket_fetcher import JiraTicketFetcher
from ticket_led_mapper import TicketLedMapper
from neo_pixel_controller import NeoPixelController

import version

LED_COUNT = 40

# Load environment variables from .env file
load_dotenv()

ticket_fetcher = JiraTicketFetcher()
ticket_led_mapper = TicketLedMapper(LED_COUNT)
neo_pixel_controller = NeoPixelController(LED_COUNT)

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
        'tickets': ticket_fetcher.get_tickets()  # Use the new class to get tickets
    })

@scheduler.task('cron', id='do_job_update_tickets', minute='*/5')
def job_update_tickets():
    ticket_fetcher.update_tickets()

@scheduler.task('interval', id='do_job_update_pixels', seconds=0.1)
def job_update_pixels():
    tickets = ticket_fetcher.get_tickets()
    ticket_led_mapper.set_ticket(tickets)
    leds = ticket_led_mapper.leds
    neo_pixel_controller.update_pixels(leds)

def cleanup():
    del neo_pixel_controller

atexit.register(cleanup)

if __name__ == '__main__':
    app.run()
