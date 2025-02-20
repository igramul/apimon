import os
import json
from collections import OrderedDict

from requests.auth import HTTPBasicAuth
from oauthlib.oauth2 import BackendApplicationClient
from requests_oauthlib import OAuth2Session

import colors

class JiraTicketFetcher:
    def __init__(self) -> None:
        self._token_url = os.environ.get('ACCESS_TOKEN_URL')
        self._client_id = os.environ.get('CLIENT_ID')
        self._client_secret = os.environ.get('CLIENT_SECRET')
        self.scope = os.environ.get('SCOPE')
        self._base_url = 'https://flow.api.sbb.ch:443/rest/api/2'
        self._status_list = ['Open', 'In Progress', 'Deferred', 'Checking']
        self._status_color_map = {
            'Checking': colors.green,
            'Deferred': colors.blue,
            'In Progress': colors.magenta,
            'Open': colors.red
        }
        self._tickets = OrderedDict()
        self._colors = OrderedDict()
        self.update_tickets()

    def _get_oauth_token(self) -> OAuth2Session:

        client = BackendApplicationClient(client_id=self._client_id)
        oauth = OAuth2Session(client=client)
        oauth.fetch_token(
            token_url=self._token_url,
            auth=HTTPBasicAuth(self._client_id, self._client_secret),
            scope=self.scope
        )
        return oauth

    def update_tickets(self):
        oauth: OAuth2Session = self._get_oauth_token()
        path: str = 'search'
        url : str = f'{self._base_url}/{path}'

        for status in self._status_list:
            jql = f'project = AITG AND component = APIM-Betrieb AND status = "{status}"'
            data = {
                'jql': jql,
                'maxResults': 0,
                'fields': ['key']
            }
            response = oauth.post(url=url, json=data)
            response_json = json.JSONDecoder().decode(response.text)
            color = self._status_color_map.get(status)
            self._tickets[status] = self._colors[color] = response_json.get('total')

    @property
    def tickets(self) -> OrderedDict:
        return self._tickets

    @property
    def colors(self) -> OrderedDict:
        return self._colors