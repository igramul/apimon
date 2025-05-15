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

git_info = GitInfo().load_json()

# Load environment variables from .env file
load_dotenv()

# Initialisiere die benötigten Komponenten
apim_ticket_fetcher = JiraTicketFetcher(name='APIM', jira_filter='project = AITG AND component = APIM-Betrieb')
apim_ticket_led_mapper = TicketLedMapper(led_count=LED_COUNT, name='APIM')
apim_neopixel_controller = NeoPixelController(led_count=LED_COUNT, gpio_pin=18, name='APIM')

kafka_ticket_fetcher = JiraTicketFetcher(name='Kafka', jira_filter='project = KAFKABETR')
kafka_ticket_led_mapper = TicketLedMapper(led_count=LED_COUNT, name='Kafka')
kafka_neopixel_controller = NeoPixelController(led_count=LED_COUNT, gpio_pin=19, name='Kafka', cycle_time_offset=1)


# Setze Konfigurationswerte für den Scheduler
class Config:
    SCHEDULER_API_ENABLED = False


logging.basicConfig(level=logging.INFO)
app = Flask(__name__)
app.config.from_object(Config())

# Initialisiere Scheduler
scheduler = APScheduler()


# Listener, der über den Ausgang der Scheduler-Tasks informiert
def scheduler_listener(event):
    if event.exception:
        logging.error(f'Scheduler task {event.job_id} failed: {event.exception}')


scheduler.add_listener(scheduler_listener, EVENT_JOB_EXECUTED | EVENT_JOB_ERROR)
scheduler.init_app(app)
scheduler.start()

logging.getLogger('apscheduler.executors.default').setLevel(logging.WARNING)


@app.route('/', methods=['GET'])
def get_api_info():
    return jsonify({
        'name': __name__,
        'git_info': {
            'version': git_info.version,
            'commit': git_info.commit,
            'branch': git_info.branch,
            'description': git_info.description
        },
        'led_stripes':
        {
            'apim': {
                'tickets': apim_ticket_fetcher.tickets,
                'leds': [str(color) for color in apim_neopixel_controller.leds],
                'status': apim_neopixel_controller.status.name,
                'overflow': apim_neopixel_controller.overflow
            },
            'kafka:': {
                'tickets': kafka_ticket_fetcher.tickets,
                'leds': [str(color) for color in kafka_neopixel_controller.leds],
                'status': kafka_neopixel_controller.status.name,
                'overflow': kafka_neopixel_controller.overflow
            }
        }
    })


# Scheduler-Task für APIM-Tickets mit erweiterter Exception-Behandlung
@scheduler.task('cron', id='do_job_update_tickets', minute='*/1')
def job_update_tickets():
    try:
        apim_ticket_fetcher.update_tickets()
        tickets = apim_ticket_fetcher.tickets
        apim_ticket_led_mapper.set_ticket(tickets)
        leds = apim_ticket_led_mapper.leds
        apim_neopixel_controller.set_leds(leds)
        overflow = apim_ticket_led_mapper.overflow
        apim_neopixel_controller.set_overflow(overflow)
        apim_neopixel_controller.set_error(False)
    except ConnectionError as ce:
        logging.error("ConnectionError beim Aktualisieren der APIM-Tickets: %s", ce)
        apim_neopixel_controller.set_connection_error(True)
    except Exception as exc:
        logging.exception("Unerwarteter Fehler beim Aktualisieren der APIM-Tickets: %s", exc)
        apim_neopixel_controller.set_error(True)
    else:
        apim_neopixel_controller.set_connection_error(False)
        apim_neopixel_controller.set_error(False)

    try:
        kafka_ticket_fetcher.update_tickets()
        tickets = kafka_ticket_fetcher.tickets
        kafka_ticket_led_mapper.set_ticket(tickets)
        leds = kafka_ticket_led_mapper.leds
        kafka_neopixel_controller.set_leds(leds)
        overflow = kafka_ticket_led_mapper.overflow
        kafka_neopixel_controller.set_overflow(overflow)
        kafka_neopixel_controller.set_error(False)
    except ConnectionError as ce:
        logging.error("ConnectionError beim Aktualisieren der Kafka-Tickets: %s", ce)
        kafka_neopixel_controller.set_connection_error(True)
    except Exception as exc:
        logging.exception("Unerwarteter Fehler beim Aktualisieren der Kafka-Tickets: %s", exc)
        kafka_neopixel_controller.set_error(True)
    else:
        kafka_neopixel_controller.set_connection_error(False)
        kafka_neopixel_controller.set_error(False)

# Scheduler-Task für das regelmässige Update der LEDs
@scheduler.task('interval', id='do_job_update_pixels', seconds=0.1)
def job_update_pixels():
    apim_neopixel_controller.update()
    kafka_neopixel_controller.update()


# Clean-up-Funktion, die beim Beenden der Anwendung ausgeführt wird
def cleanup():
    scheduler.shutdown()
    apim_neopixel_controller.clear()
    kafka_neopixel_controller.clear()

atexit.register(cleanup)

# Initialer Aufruf der Ticket-Updates, um beim Start den aktuellen Status zu erhalten
job_update_tickets()

if __name__ == '__main__':
    app.run()
