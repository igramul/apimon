import os
import json
import logging

from flask import Flask, jsonify
from flask_apscheduler import APScheduler
from dotenv import load_dotenv
from oauthlib.oauth2 import BackendApplicationClient
from requests.auth import HTTPBasicAuth
from requests_oauthlib import OAuth2Session

import version

# Load environment variables from .env file
load_dotenv()

tickets = {}

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


@app.route('/')
def get_root():
    return jsonify({
        'name': 'apimon',
        'version': version.version,
        'tickets': tickets
    })


def _update_tickets():
    token_url = os.environ.get('ACCESS_TOKEN_URL')
    client_id = os.environ.get('CLIENT_ID')
    client_secret = os.environ.get('CLIENT_SECRET')
    scope = os.environ.get('SCOPE')

    # Create a BackendApplicationClient object
    client = BackendApplicationClient(client_id=client_id)

    # Create an OAuth2Session object
    oauth = OAuth2Session(client=client)
    # Get the access token
    token = oauth.fetch_token(
        token_url=token_url,
        auth=HTTPBasicAuth(client_id, client_secret),
        scope=scope
    )

    base_url = 'https://flow.api.sbb.ch:443/rest/api/2'
    path = 'search'

    url = f'{base_url}/{path}'

    status_list = ['Open', 'In Progress', 'Deferred', 'Checking']

    for status in status_list:

        jql = f'project = AITG AND component = APIM-Betrieb AND status = "{status}"'

        data = {
            'jql': jql,
            'maxResults': 0,
            'fields': ['key']
        }

        response = oauth.post(url=url, json=data)
        response_json = json.JSONDecoder().decode(response.text)
        tickets[status] = response_json.get('total')


@scheduler.task('cron', id='do_job_update_tickets', minute='*/5')
def job_update_tickets():
    _update_tickets()

_update_tickets()

if __name__ == '__main__':
    app.run()
