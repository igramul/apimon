import os
import json
import logging
from requests.auth import HTTPBasicAuth
from oauthlib.oauth2 import BackendApplicationClient
from requests_oauthlib import OAuth2Session


class JiraTicketFetcher:
    def __init__(self):
        self.token_url = os.environ.get('ACCESS_TOKEN_URL')
        self.client_id = os.environ.get('CLIENT_ID')
        self.client_secret = os.environ.get('CLIENT_SECRET')
        self.scope = os.environ.get('SCOPE')
        self.base_url = 'https://flow.api.sbb.ch:443/rest/api/2'
        self.status_list = ['Open', 'In Progress', 'Deferred', 'Checking']
        self.tickets = {}

    def _get_oauth_token(self):
        client = BackendApplicationClient(client_id=self.client_id)
        oauth = OAuth2Session(client=client)
        token = oauth.fetch_token(
            token_url=self.token_url,
            auth=HTTPBasicAuth(self.client_id, self.client_secret),
            scope=self.scope
        )
        return oauth

    def update_tickets(self):
        oauth = self._get_oauth_token()
        path = 'search'
        url = f'{self.base_url}/{path}'

        for status in self.status_list:
            jql = f'project = AITG AND component = APIM-Betrieb AND status = "{status}"'
            data = {
                'jql': jql,
                'maxResults': 0,
                'fields': ['key']
            }
            response = oauth.post(url=url, json=data)
            response_json = json.JSONDecoder().decode(response.text)
            self.tickets[status] = response_json.get('total')

    def get_tickets(self):
        return self.tickets
