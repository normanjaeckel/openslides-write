from typing import Dict, List

import requests
import simplejson as json
from werkzeug.exceptions import BadRequest, InternalServerError

from ..utils.types import ServiceConfig


class Sequencer:
    """
    Adapter to connect to sequencer.
    """

    def __init__(self, config: ServiceConfig) -> None:
        self.url = f"{config['protocol']}://{config['host']}:{config['port']}"
        self.headers = {"Content-Type": "application/json"}

    def get(self, keys: Dict[str, int]) -> Dict[str, List[int]]:
        """
        Fetches one or more new ids for every given key from the sequencer. The
        value of each key in the keys dictionary is a number of how many ids are
        requested.
        """
        response = requests.post(self.url, data=json.dumps(keys), headers=self.headers,)
        if not response.ok:
            raise InternalServerError("Connection to sequencer failed.")
        return response.json()
