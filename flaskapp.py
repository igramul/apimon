import os
import json
import logging
import atexit

from flask import Flask, jsonify
from flask_apscheduler import APScheduler
from dotenv import load_dotenv
from oauthlib.oauth2 import BackendApplicationClient
from requests.auth import HTTPBasicAuth
from requests_oauthlib import OAuth2Session

import board
import neopixel

import colors
import version

# Load environment variables from .env file
load_dotenv()

pixels = neopixel.NeoPixel(board.D18, 30)

tickets = {}

# set configuration values
class Config:
    SCHEDULER_API_ENABLED = True

logging.basicConfig(level=logging.INFO)
app = Flask(__name__)
app.config.from_object(Config())

def cleanup():
    print('Das Programm apimon wird beendet. Alle LEDs werde gelöscht.')
    del pixels

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
        'tickets': tickets
    })

status_list = ['Open', 'In Progress', 'Deferred', 'Checking']
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


status_color_map = {
    'Checking': colors.green,
    'Deferred': colors.blue,
    'In Progress': colors.magenta,
    'Open': colors.red
}

pixel_array = [colors.black, 10]
def _update_pixels():
    index = 0
    if pixel_array[0] == colors.weiss:
        pixel_array[0] = colors.black
    else:
         pixel_array[0] = colors.weiss
    pixels[index] = pixel_array[0]

    pixel_array[1] = pixel_array[1] + 1
    if pixel_array[1] < 10:
        pixels.show()
        return
    pixel_array[1] = 0

    index =+ 1
    for status in reversed(status_list):
        count = tickets.get(status)
        if not count:
            continue
        color = status_color_map.get(status)
        for i in range(count):
            pixels[index+i] = color
        index += count
        for i in range(index, pixels.n):
            pixels[i] = colors.black
    pixels.show()


@scheduler.task('cron', id='do_job_update_tickets', minute='*/5')
def job_update_tickets():
    _update_tickets()


@scheduler.task('interval', id='do_job_update_pixels', seconds=1)
def job_update_pixels():
   _update_pixels() 


_update_tickets()

if __name__ == '__main__':
    app.run()
