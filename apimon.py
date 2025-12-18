import logging
import atexit

from flask import Flask, jsonify
from flask_apscheduler import APScheduler
from apscheduler.events import EVENT_JOB_EXECUTED, EVENT_JOB_ERROR
from dotenv import load_dotenv

from app.JTLS import JiraTicketLedStripeList

from app.gitinfo import GitInfo

LED_COUNT = 40

git_info = GitInfo().load_json()

# Load environment variables from .env file
load_dotenv()

# Initialisiere die benötigten Komponenten
jira_tickets_led_stripes = JiraTicketLedStripeList()


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
        'led_stripes': jira_tickets_led_stripes.get_info_dict(),
    })


# Scheduler-Task für APIM-Tickets mit erweiterter Exception-Behandlung
@scheduler.task('cron', id='do_job_update_tickets', minute='*/1')
def job_update_tickets():
    jira_tickets_led_stripes.update_tickets()


# Scheduler-Task für das regelmässige Update der LEDs
@scheduler.task('interval', id='do_job_update_pixels', seconds=0.1)
def job_update_pixels():
    try:
        jira_tickets_led_stripes.update_pixels()
    except Exception as e:
        logging.error(f"Error in job_update_pixels: {e}", exc_info=True)


# Clean-up-Funktion, die beim Beenden der Anwendung ausgeführt wird
def cleanup():
    scheduler.shutdown()
    jira_tickets_led_stripes.clear()


atexit.register(cleanup)

# Initialer Aufruf der Ticket-Updates, um beim Start den aktuellen Status zu erhalten
jira_tickets_led_stripes.update_tickets()

if __name__ == '__main__':
    app.run()
