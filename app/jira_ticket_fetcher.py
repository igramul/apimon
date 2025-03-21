import time
from typing import List, Dict
import logging
import os
import json
from collections import OrderedDict

from requests.exceptions import ConnectionError
from requests.auth import HTTPBasicAuth
from oauthlib.oauth2 import BackendApplicationClient
from requests_oauthlib import OAuth2Session

from .models.color import Color


class JiraTicketFetcher:

    TIMEOUT: int = 60*60  # 1h
    STATUS_LIST: List[str] = ['Open', 'In Progress', 'Deferred', 'Checking']
    STATUS_TIMEOUT_MAP: Dict[str, str] = {
        'Open': '-3h',
        'In Progress': '-7d',
        'Deferred': '-14d',
        'Checking': '-5w'
    }
    STATUS_COLOR_MAP: Dict[str, Color] = {
        'Checking': Color.green,
        'Deferred': Color.blue,
        'In Progress': Color.magenta,
        'Open': Color.red
    }

    def __init__(self) -> None:
        self._token_url: str = os.environ.get('ACCESS_TOKEN_URL')
        self._client_id: str = os.environ.get('CLIENT_ID')
        self._client_secret: str = os.environ.get('CLIENT_SECRET')
        self.scope: str = os.environ.get('SCOPE')
        self._base_url: str = os.environ.get('BASE_URL')

        self._tickets: OrderedDict[str, str] = OrderedDict()
        self._colors: OrderedDict[Color, str] = OrderedDict()
        self._timeouts: OrderedDict[str, str] = OrderedDict()
        self._last_update: float = time.time()

        try:
            self.update_tickets()
        except ConnectionError as e:
            logging.error(e)

    def _get_oauth_token(self) -> OAuth2Session:

        client = BackendApplicationClient(client_id=self._client_id)
        oauth = OAuth2Session(client=client)
        try:
            oauth.fetch_token(
                token_url=self._token_url,
                auth=HTTPBasicAuth(self._client_id, self._client_secret),
                scope=self.scope
            )
        except ConnectionError:
            if not self.data_still_valid:
                self._tickets = OrderedDict()
                self._colors = OrderedDict()
            raise ConnectionError('Could not get OAuth token.')
        return oauth

    def update_tickets(self):
        oauth: OAuth2Session = self._get_oauth_token()
        path: str = 'search'
        url: str = f'{self._base_url}/{path}'

        for status in self.STATUS_LIST:
            jql = f'project = AITG AND component = APIM-Betrieb AND status = "{status}"'
            data = {
                'jql': jql,
                'maxResults': 0,
                'fields': ['key']
            }
            try:
                response = oauth.post(url=url, json=data)
            except ConnectionError:
                if not self.data_still_valid:
                    self._tickets = OrderedDict()
                    self._colors = OrderedDict()
                raise ConnectionError(f'Could not access Jira: POST {url}, {data}')
            response_json = json.JSONDecoder().decode(response.text)
            color = self.STATUS_COLOR_MAP.get(status)
            self._tickets[status] = self._colors[color] = response_json.get('total')

        for status in self.STATUS_LIST:
            timeout = self.STATUS_TIMEOUT_MAP.get(status)
            jql = f'project = AITG AND component = APIM-Betrieb AND status = "{status}" AND created <= {timeout}'
            data = {
                'jql': jql,
                'maxResults': 0,
                'fields': ['key']
            }
            try:
                response = oauth.post(url=url, json=data)
            except ConnectionError:
                if not self.data_still_valid:
                    self._timeouts = OrderedDict()
                raise ConnectionError(f'Could not access Jira: POST {url}, {data}')
            response_json = json.JSONDecoder().decode(response.text)
            self._timeouts[status] = response_json.get('total')

        self._last_update = time.time()

    @property
    def tickets(self) -> OrderedDict:
        return self._tickets

    @property
    def colors(self) -> OrderedDict:
        return self._colors

    @property
    def timeouts(self) -> OrderedDict:
        return self._timeouts

    @property
    def data_still_valid(self) -> bool:
        return self._last_update + self.TIMEOUT > time.time()
