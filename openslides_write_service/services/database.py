from typing import Dict, List, Tuple

import grpc
import requests
import simplejson as json
from database.database_pb2 import (
    GetElementsRequest,
    GetElementsResponse,
    SaveReply,
    SaveRequest,
)
from database.database_pb2_grpc import DatabaseStub
from werkzeug.exceptions import InternalServerError
from database.database_pb2_grpc import DatabaseStub
from database.database_pb2 import (
    SaveRequest,
    SaveReply,
    GetElementsRequest,
    GetElementsResponse,
)


class Database:
    """
    Adapter to connect to (read-only) database.
    """

    def __init__(self, database_url: str) -> None:
        self.stub = DatabaseStub(grpc.insecure_channel(database_url))

    def get(self, *keys: str, version: int = 0) -> Tuple[str, int]:
        """
        Fetches all data for given keys from database.
        """
        request = GetElementsRequest(keys=keys, version=version)
        response = self.stub.getElements(request)
        return response.data, response.version

    def send(self, version: int, keys: List[str], data: Dict[str, str]) -> int:
        """
        Sends one or more key-value pairs to event writer service.

        The keys list are the ones that have been read on given version to
        calculate the data (dictionary of keys and values) that should be
        written to event stream.
        """
        request = SaveRequest(version=version, depends=keys, data=data)
        response = self.stub.save(request)
        return response.version
