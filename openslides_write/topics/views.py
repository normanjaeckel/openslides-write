from typing import Callable, Iterable

import requests
import simplejson as json
from werkzeug.exceptions import BadRequest, InternalServerError
from werkzeug.routing import Map
from werkzeug.wrappers import Request, Response

from ..utils.routing import Rule
from ..utils.types import ServicesConfig
from .schema import is_valid_new_topic, is_valid_update_topic


class TopicViewSet:
    """
    Viewset for topics.

    During initialization we bind the viewpoint and database to the instance.
    """

    def __init__(self, viewpoint: str, services: ServicesConfig) -> None:
        self.viewpoint = viewpoint

        self.database_url = f"{services['database']['protocol']}://{services['database']['host']}:{services['database']['port']}"
        self.database_headers = {"Content-Type": "application/json"}
        self.writer_url = "X"
        self.writer_headers = {"Content-Type": "application/json"}
        self.get_id_url = "Y"
        self.get_id_headers = {"Content-Type": "application/json"}

    def dispatch(self, request: Request, **kwargs: dict) -> Response:
        """
        Dispatches request to the viewpoint.
        """
        if not request.is_json:
            raise BadRequest(
                "Wrong media type. Use 'Content-Type: application/json' instead."
            )
        return getattr(self, self.viewpoint)(request, **kwargs)

    def new(self, request: Request, **kwargs: dict) -> Response:
        """
        Viewpoint to create new topics.
        """
        event_id = kwargs["event"]

        # TODO: Check permissions.
        data = request.json
        is_valid_new_topic(data)
        result = {"created": 0, "error": 0}

        # Check existence of event.
        response = requests.get(
            self.database_url,
            data=json.dumps([f"event.{event_id}"]),
            headers=self.database_headers,
        )
        if not response.ok:
            raise InternalServerError("Connection to database failed.")
        if not response.json()["data"]:
            raise BadRequest(f"Event with id {event_id} does not exist.")
        change_id = response.json()["changeId"]

        # Parse topics
        for topic in data:
            # Get new id.
            how_many = 1
            response = requests.post(
                self.get_id_url,
                data=json.dumps({f"event.{event_id}.topic": how_many}),
                headers=self.get_id_headers,
            )
            if not response.ok:
                result["error"] += 1
                continue
            topic_id = response.text

            # Write data to stream.
            data = {
                "changeId": change_id,
                "keys": f"event.{event_id}",
                "data": {
                    f"event.{event_id}.topic.{topic_id}.title": topic.title,
                    f"event.{event_id}.topic.{topic_id}.text": topic.text,
                    f"event.{event_id}.topic.{topic_id}.attachments": topic.attachments,
                },
            }
            response = requests.post(
                self.writer_url, data=json.dumps(data), headers=self.writer_headers
            )
            if response.ok:
                result["created"] += 1
            else:
                result["error"] += 1
        return Response(json.dumps(result), status=201, content_type="application/json")

    def update(self, request: Request, **kwargs: dict) -> Response:
        """
        Viewpoint to update existing topics.
        """
        # TODO: Check permissions.
        data = request.json
        is_valid_update_topic(data)
        result = {"updated": 0, "error": 0}
        for topic in data:
            id = topic.pop("id")
            rev = topic.pop("rev")
            url = "/".join((self.database_url, id))
            headers = self.database_headers
            headers["If-Match"] = rev
            response = requests.put(url, data=json.dumps(topic), headers=headers)
            if response.ok:
                result["updated"] += 1
            else:
                result["error"] += 1
        return Response(json.dumps(result), status=200, content_type="application/json")

    def delete(self, request: Request, **kwargs: dict) -> Response:
        """
        Viewpoint to delete existing topics.
        """
        return Response("Hello")


def get_get_rules_func(services: ServicesConfig) -> Callable[[Map], Iterable[Rule]]:
    """
    Contructor for get_rules method.
    """

    def get_rules(map: Map) -> Iterable[Rule]:
        """
        Rules for this app.
        """
        return [
            Rule(
                "/<int:event>/topics/new",
                endpoint="TopicViewSet new",
                methods=("POST",),
                view=TopicViewSet("new", services=services),
            ),
            Rule(
                "/<int:event>/topics/update",
                endpoint="TopicViewSet update",
                methods=("POST",),
                view=TopicViewSet("update", services=services),
            ),
            Rule(
                "/<int:event>/topics/delete",
                endpoint="TopicViewSet delete",
                methods=("POST",),
                view=TopicViewSet("delete", services=services),
            ),
        ]

    return get_rules
