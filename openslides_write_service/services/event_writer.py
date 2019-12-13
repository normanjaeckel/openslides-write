from typing import Any, Dict, List

import requests
import simplejson as json
from werkzeug.exceptions import InternalServerError


class EventWriter:
    """
    Adapter to connect to event writer.
    """

    def __init__(self, event_writer_url: str) -> None:
        self.url = event_writer_url
        self.headers = {"Content-Type": "application/json"}

    def send(self, version: int, keys: List[str], data: Dict[str, Any]) -> None:
        """
        Sends one or more key-value pairs to event writer service.

        The keys list are the ones that have been read on given version to
        calculate the data (dictionary of keys and values) that should be
        written to event stream.
        """
        data = {
            "version": version,
            "depends": keys,
            "data": data,
        }
        response = requests.post(self.url, data=json.dumps(data), headers=self.headers)
        if not response.ok:
            raise InternalServerError("Connection to event writer failed.")
