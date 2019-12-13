from typing import Tuple

import requests
import simplejson as json
from werkzeug.exceptions import BadRequest, InternalServerError

from ..utils.types import ServiceConfig


class Database:
    """
    Adapter to connect to (read-only) database.
    """

    def __init__(self, config: ServiceConfig) -> None:
        self.url = f"{config['protocol']}://{config['host']}:{config['port']}"
        self.headers = {"Content-Type": "application/json"}

    def get(self, *keys: str) -> Tuple[str, int]:
        """
        Fetches all data for given keys from database.
        """
        response = requests.get(self.url, data=json.dumps(keys), headers=self.headers,)
        if not response.ok:
            raise InternalServerError("Connection to database failed.")
        return response.json()["data"], response.json()["changeId"]
