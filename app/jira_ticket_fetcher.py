import os
import json
from collections import OrderedDict

import requests
from requests.exceptions import ConnectionError
from requests.auth import HTTPBasicAuth
from oauthlib.oauth2 import BackendApplicationClient
from requests_oauthlib import OAuth2Session

from .models.color import Color


class JiraTicketFetcher:
    def __init__(self) -> None:
        self._token_url = os.environ.get('ACCESS_TOKEN_URL')
        self._client_id = os.environ.get('CLIENT_ID')
        self._client_secret = os.environ.get('CLIENT_SECRET')
        self.scope = os.environ.get('SCOPE')
        self._base_url = os.environ.get('BASE_URL')
        self._status_list = ['Open', 'In Progress', 'Deferred', 'Checking']
        self._status_color_map = {
            'Checking': Color.green,
            'Deferred': Color.blue,
            'In Progress': Color.magenta,
            'Open': Color.red
        }
        self._tickets = OrderedDict()
        self._colors = OrderedDict()
        self.update_tickets()

    def _get_oauth_token(self) -> OAuth2Session:

        client = BackendApplicationClient(client_id=self._client_id)
        oauth = OAuth2Session(client=client)
        try:
            oauth.fetch_token(
                token_url=self._token_url,
                auth=HTTPBasicAuth(self._client_id, self._client_secret),
                scope=self.scope
            )
        except requests.exceptions.ConnectionError:
            raise ConnectionError('Could not get OAuth token.')
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
            try:
                response = oauth.post(url=url, json=data)
            except requests.exceptions.ConnectionError:
                raise ConnectionError('Could not get Jira tickets.')
            response_json = json.JSONDecoder().decode(response.text)
            color = self._status_color_map.get(status)
            self._tickets[status] = self._colors[color] = response_json.get('total')

    @property
    def tickets(self) -> OrderedDict:
        return self._tickets

    @property
    def colors(self) -> OrderedDict:
        return self._colors