import time
from typing import Dict
import logging
import os
import json
from collections import OrderedDict

from requests.exceptions import ConnectionError
from requests.auth import HTTPBasicAuth
from oauthlib.oauth2 import BackendApplicationClient
from requests_oauthlib import OAuth2Session


class JiraTicketFetcher:

    TIMEOUT: int = 60*60  # 1h
    STATUS_MAP: Dict[str, Dict[str, str]] = {
        'Open': {
            'color': '(255, 0, 0)',
            'timeout': '3h',
        },
        'In Progress': {
            'color': '(255, 0, 255)',
            'timeout': '1w',
        },
        'Deferred': {
            'color': '(0, 0, 255)',
            'timeout': '4w',
        },
        'Checking': {
            'color': '(0, 255, 0)',
            'timeout': '6w',
        },
    }

    def __init__(self, name: str, jira_filter: str) -> None:
        self.logger = logging.getLogger(f'{__name__}.{name}')
        self._token_url: str = os.environ.get('ACCESS_TOKEN_URL')
        self._client_id: str = os.environ.get('CLIENT_ID')
        self._client_secret: str = os.environ.get('CLIENT_SECRET')
        self.scope: str = os.environ.get('SCOPE')
        self._base_url: str = os.environ.get('BASE_URL')

        self.name = name
        self.jira_filter = jira_filter

        self._tickets: OrderedDict[str, dict] = OrderedDict()
        self._last_update: float = time.time()

        try:
            self.update_tickets()
        except ConnectionError as e:
            self.logger.error(e)

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
            self.logger.debug(f'Could not get OAuth token for client_id: {self._client_id}')
            if not self.data_still_valid:
                self._tickets = OrderedDict()
                self._colors = OrderedDict()
            raise ConnectionError('Could not get OAuth token.')
        return oauth

    def update_tickets(self):
        oauth: OAuth2Session = self._get_oauth_token()
        path: str = 'search'
        url: str = f'{self._base_url}/{path}'

        try:
            for status in self.STATUS_MAP.keys():
                self._tickets[status] = self.STATUS_MAP.get(status)
                jql_status = f'{self.jira_filter} AND status = "{status}"'
                data = {
                    'jql': jql_status,
                    'maxResults': 0,
                    'fields': ['key']
                }
                response_status = oauth.post(url=url, json=data)
                response_status_json = json.JSONDecoder().decode(response_status.text)
                total_status = response_status_json.get('total')
                self.logger.debug(f'Total Jira tickets {status}: {total_status}')
                self._tickets[status]['count'] = total_status

                timeout = self._tickets[status].get('timeout')
                jql_timeout = f'{jql_status} AND created <= -{timeout}'
                data = {
                    'jql': jql_timeout,
                    'maxResults': 0,
                    'fields': ['key']
                }
                response_timeout = oauth.post(url=url, json=data)
                response_timeout_json = json.JSONDecoder().decode(response_timeout.text)
                total_timeout = response_timeout_json.get('total')
                self.logger.debug(f'Overdue Jira tickets {status}: {total_timeout}')
                self._tickets[status]['overdue'] = total_timeout

        except ConnectionError:
            self.logger.debug(f'Could not access {self.name} Jira at: {url}')
            if not self.data_still_valid:
                self._tickets = OrderedDict()
            raise ConnectionError(f'Could not access Jira: {url}')

        self._last_update = time.time()

    @property
    def tickets(self) -> OrderedDict:
        return self._tickets

    @property
    def data_still_valid(self) -> bool:
        return self._last_update + self.TIMEOUT > time.time()
