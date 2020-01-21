"""
   This is the base of Conversus API SDK.
"""

import requests
import json

from Conversus.config import ConversusRequestConfig

__author__ = "Anthony Bu"
__copyright__ = "Copyright 2019, Converseon"


class ConversusConnection(object):
    def __init__(self, config: ConversusRequestConfig):
        self.config = config
        self.logger = self.config.logger
        self.core_models = {}
        self.custom_models = {}
        if self.validate_api_key(self.config.api_key):
            self.refresh_core_model_list(self.config.api_key)
            self.refresh_custom_model_list(self.config.api_key)

    def __str__(self):
        return 'ConversusAPI({})'.format(self.config.api_key)

    def _call_api(self, method: str, endpoint: str, return_json: bool = True):
        try:
            req = getattr(requests, method)
        except AttributeError:
            raise ValueError('Method {} not found.'.format(method))
        self.logger.debug('Calling API: [{}], {}'.format(method, endpoint))
        response = req(self.config.base_url + endpoint)
        self.logger.debug('API response: status_code {}, size {}'.format(response.status_code, len(response.content)))

        if response.status_code == 200:
            if return_json:
                return json.loads(response.text)
            else:
                return response.text
        else:
            raise RuntimeError('Conversus API Error')

    def validate_api_key(self, api_key: str, raise_on_invalid=False) -> bool:
        self.logger.debug('Validating API key {}'.format(api_key))
        response = self._call_api('get', 'auth/verify_api_key?api_key={}'.format(api_key))
        if response['validation']:
            self.logger.info('API key {} validated.'.format(api_key))
            return True
        else:
            self.logger.error('API key {} failed validation.'.format(api_key))
            if raise_on_invalid:
                raise ValueError('Invalid API Key')
        return False

    def refresh_core_model_list(self, api_key: str) -> None:
        self.logger.debug('Refreshing core model list...')
        self.core_models = self._call_api('get', 'auth/list_core_classifiers?api_key={}'.format(api_key))
        self.logger.debug('Core model list {}'.format(self.core_models))

    def refresh_custom_model_list(self, api_key: str) -> None:
        self.logger.debug('Refreshing custom model list...')
        self.custom_models = self._call_api('get', 'auth/list_custom_classifiers?api_key={}'.format(api_key))
        self.logger.debug('Custom model list {}'.format(self.custom_models))
