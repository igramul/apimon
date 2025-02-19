import logging
import atexit

from flask import Flask, jsonify
from flask_apscheduler import APScheduler
from dotenv import load_dotenv

import version

from jira_ticket_fetcher import JiraTicketFetcher  # Import the JiraTicketFetcher class
from neo_pixel_controller import NeoPixelController  # Import the NeoPixelController class

# Load environment variables from .env file
load_dotenv()

# Initialize JiraTicketFetcher
ticket_fetcher = JiraTicketFetcher()

# Initialize NeoPixelController
neo_pixel_controller = NeoPixelController()

# set configuration values
class Config:
    SCHEDULER_API_ENABLED = True

logging.basicConfig(level=logging.INFO)
app = Flask(__name__)
app.config.from_object(Config())

def cleanup():
    del neo_pixel_controller

atexit.register(cleanup)

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

@scheduler.task('interval', id='do_job_update_pixels', seconds=1)
def job_update_pixels():
    neo_pixel_controller.update_pixels(ticket_fetcher.get_tickets(), ticket_fetcher.status_list)

ticket_fetcher.update_tickets()

if __name__ == '__main__':
    app.run()
