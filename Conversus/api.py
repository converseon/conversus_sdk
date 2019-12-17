"""
   This is the base of Conversus API SDK.
"""

import requests
import json

import random

__author__ = "Anthony Bu"
__copyright__ = "Copyright 2019, Converseon"


class ConversusConnection(object):
    def __init__(self, api_key: str, dev=False):
        self.api_key = api_key
        self.core_models = {}
        self.custom_models = {}
        self.base_url = "http://staging.app.conversus.ai/api/" if dev else "http://app.conversus.ai/api/"
        if self.validate_api_key(self.api_key):
            self.refresh_core_model_list(self.api_key)
            self.refresh_custom_model_list(self.api_key)

    def __str__(self):
        return 'ConversusAPI({})'.format(self.api_key)

    def validate_api_key(self, api_key: str) -> bool:
        response = requests.get(self.base_url + 'auth/verify_api_key?api_key={}'.format(api_key))
        if response.status_code == 200:
            json_data = json.loads(response.text)
            if json_data['validation']:
                return True
            else:
                raise ValueError('Invalid API Key')
        else:
            raise RuntimeError('Conversus API Error')

    def refresh_core_model_list(self, api_key: str) -> None:
        self.core_models = requests.get(self.base_url + 'auth/list_core_classifiers?api_key={}'.format(api_key))

    def refresh_custom_model_list(self, api_key: str) -> None:
        self.custom_models = requests.get(self.base_url + 'auth/list_custom_classifiers?api_key={}'.format(api_key))
