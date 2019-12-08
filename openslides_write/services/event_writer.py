from typing import Any, Dict, List

import requests
import simplejson as json
from werkzeug.exceptions import BadRequest, InternalServerError

from ..utils.types import ServiceConfig


class EventWriter:
    """
    Adapter to connect to event writer.
    """

    def __init__(self, config: ServiceConfig) -> None:
        self.url = f"{config['protocol']}://{config['host']}:{config['port']}"
        self.headers = {"Content-Type": "application/json"}

    def send(self, change_id: int, keys: List[str], data: Dict[str, Any]) -> None:
        """
        Sends one or more key-value pairs to event writer service.

        The keys list are the ones that have been read on given change_id to
        calculate the data (dictionary of keys and values) that should be
        written to event stream.
        """
        data = {
            "changeId": change_id,
            "keys": keys,
            "data": data,
        }
        response = requests.post(self.url, data=json.dumps(data), headers=self.headers)
        if not response.ok:
            raise InternalServerError("Connection to sequencer failed.")
