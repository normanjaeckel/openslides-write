import logging
from typing import Iterable

import simplejson as json
from werkzeug.exceptions import BadRequest
from werkzeug.wrappers import Request, Response

from .actions import action_map
from .services.database import Database
from .services.event_store import EventStoreAdapter
from .utils.schema import action_view_schema
from .utils.types import Environment, Event

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
            self.handle_error(
                MediaTypeException(
                    "Wrong media type. Use 'Content-Type: application/json' instead."
                )
            )
        action_requests = request.json
        try:
            self.validate(action_requests)
        except JsonSchemaException as exception:
            self.handle_error(exception)

        # Parse actions and creates events
        try:
            events = self.parse_actions(action_requests)
        except ActionException as exception:
            self.handle_error(exception)

        # Send events to database
        try:
            self.event_store.send(events)
        except EventStoreException as exception:
            self.handle_error(exception)

        result = []  # TODO

        return Response(json.dumps(result), content_type="application/json")

    def validate(self, action_requests: List[Dict]) -> None:
        """
        Validates action_requests sent by client.

        Raises JsonSchemaException if input is invalid.
        """
        action_view_schema(action_requests)

    def parse_actions(self, action_requests: List[Dict]) -> Iterable[Event]:
        """
        Parses action requests send by client
        """
        events = []
        for element in action_requests:
            action = action_map.get(element["action"])
            if action is None:
                raise BadRequest(f"Action {element['action']} does not exist.")
            logger.debug(f"Perform action {element['action']}")
            event = action().perform(element["data"])
            events.append(event)
        return events

    def handle_error(self, exception: Exception) -> None:
        """
        Handles some exceptions during dispatch of request. Raises HTTP 400.
        """
        logger.debug(f"Error in view. Exception message is {exception.message}")
        raise BadRequest(exception.message)
