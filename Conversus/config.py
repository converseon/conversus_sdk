"""
   This constructs the Conversus request config object required for API calls.
"""

import logging
import sys

__author__ = "Anthony Bu"
__copyright__ = "Copyright 2019, Converseon"


class ConversusRequestConfig(object):
    def __init__(self, api_key: str, base_url_override: str = None, logging_level=logging.INFO, dev: bool = False):
        self.api_key = api_key
        if base_url_override:
            self.base_url = base_url_override
        else:
            self.base_url = "http://staging.app.conversus.ai/api/" if dev else "http://app.conversus.ai/api/"

        logging.basicConfig(stream=sys.stdout,
                            format='%(asctime)s [Conversus API] %(levelname)s - %(message)s',
                            level=logging_level)
        self.logger = logging.getLogger('ConversusAPI')
