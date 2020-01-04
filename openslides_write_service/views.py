from typing import Iterable

import logging

import simplejson as json
from werkzeug.exceptions import BadRequest
from werkzeug.wrappers import Request, Response

from .actions import get_action_map
from .services.database import Database
from .services.event_store import EventStore
from .utils.types import Environment, Event
from .utils.schema import action_view_schema

logger = logging.getLogger(__name__)


class ActionView:
    """
    During initialization we bind the viewpoint and services to the instance.
    """

    def __init__(self, environment: Environment) -> None:
        self.database = Database(environment["database_url"])
        self.event_store = EventStore(environment["event_store_url"])

    def dispatch(self, request: Request, **kwargs: dict) -> Response:
        """
        Dispatches request to the viewpoint.
        """
        logger.debug("Start dispatching request")

        # Validate payload of request
        if not request.is_json:
            raise BadRequest(
                "Wrong media type. Use 'Content-Type: application/json' instead."
            )
        action_elements = request.json
        self.validate(action_elements)

        # Parse actions and validate them
        events = self.parse_actions(action_elements)

        # Execute actions
        self.event_store.send(events)

        result = []

        return Response(json.dumps(result), content_type="application/json")

    def validate(self, data) -> None:
        """
        Validate data send by client.
        """
        action_view_schema(data)

    def parse_actions(self, action_elements) -> Iterable[Event]:
        """
        """
        events = []
        action_map = get_action_map()
        for element in action_elements:
            action = action_map.get(element["action"])
            if action is None:
                raise BadRequest(f"Action {element['action']} does not exist.")
            events.append(action().validate(element["data"]))
        return events
