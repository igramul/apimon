import logging
import atexit

from flask import Flask, jsonify
from flask_apscheduler import APScheduler
from apscheduler.events import EVENT_JOB_EXECUTED, EVENT_JOB_ERROR
from dotenv import load_dotenv
from requests.exceptions import ConnectionError

from app.jira_ticket_fetcher import JiraTicketFetcher
from app.ticket_led_mapper import TicketLedMapper
from app.gitinfo import GitInfo

from app.neopixel_controller import NeoPixelController

LED_COUNT = 40

git_info = GitInfo()

# Load environment variables from .env file
load_dotenv()

ticket_fetcher = JiraTicketFetcher()
ticket_led_mapper = TicketLedMapper(LED_COUNT)
neopixel_controller = NeoPixelController(LED_COUNT)


# set configuration values
class Config:
    SCHEDULER_API_ENABLED = False


logging.basicConfig(level=logging.INFO)
app = Flask(__name__)
app.config.from_object(Config())

# initialize scheduler
scheduler = APScheduler()


def scheduler_listener(event):
    if event.exception:
        logging.error(f"Scheduler task {event.job_id} failed: {event.exception}")
        neopixel_controller.set_error(True)
    else:
        neopixel_controller.set_error(False)


scheduler.add_listener(scheduler_listener, EVENT_JOB_EXECUTED | EVENT_JOB_ERROR)
scheduler.init_app(app)
scheduler.start()

logging.getLogger('apscheduler.executors.default').setLevel(logging.WARNING)


@app.route('/', methods=['GET'])
def get_api_info():
    return jsonify({
        'name': __name__,
        'git_info': {
            'version': git_info.description,
            'commit': git_info.commit,
            'branch': git_info.branch,
        },
        'tickets': ticket_fetcher.tickets,
        'leds': [color.tuple_str for color in neopixel_controller.leds],
        'status': neopixel_controller.status.name,
        'overflow': neopixel_controller.overflow,
    })


@scheduler.task('cron', id='do_job_update_tickets', minute='*/1')
def job_update_tickets():
    try:
        ticket_fetcher.update_tickets()
    except ConnectionError as e:
        logging.error(e)
        neopixel_controller.set_connection_error(True)
    else:
        neopixel_controller.set_connection_error(False)
    colors = ticket_fetcher.colors
    ticket_led_mapper.set_ticket(colors)
    leds = ticket_led_mapper.leds
    neopixel_controller.set_leds(leds)
    overflow = ticket_led_mapper.overflow
    neopixel_controller.set_overflow(overflow)

@scheduler.task('interval', id='do_job_update_pixels', seconds=0.1)
def job_update_pixels():
    neopixel_controller.update()


def cleanup():
    scheduler.shutdown()


atexit.register(cleanup)

job_update_tickets()

if __name__ == '__main__':
    app.run()
