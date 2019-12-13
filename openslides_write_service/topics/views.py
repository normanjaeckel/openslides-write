from typing import Callable, Iterable

import simplejson as json
from werkzeug.exceptions import BadRequest, InternalServerError
from werkzeug.routing import Map
from werkzeug.wrappers import Request, Response

from ..utils.routing import Rule
from ..utils.types import ServicesConfig
from ..utils.views import ViewSet
from .schema import is_valid_new_topic, is_valid_update_topic


class TopicViewSet(ViewSet):
    """
    Viewset for topics.
    """

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
        event, version = self.database.get(f"event:{event_id}:name")
        if event is None:
            raise BadRequest(f"Event with id {event_id} does not exist.")

        # Parse topics
        for topic in data:
            # Get new id.
            how_many = 1  # TODO: Enable other values than 1.
            key = f"event.{event_id}.topics.topic"
            try:
                res = self.sequencer.get({key: how_many})
            except InternalServerError:
                result["error"] += 1
                continue
            topic_id = res[key][0]

            # Write data to stream.
            data = {
                f"topic:{topic_id}:title": topic["title"],
                f"topic:{topic_id}:event": event_id,
                f"topic:{topic_id}:text": topic.get("text"),
                f"topic:{topic_id}:attachments": topic.get("attachments"),
            }
            try:
                self.event_writer.send(version, [f"event:{event_id}:name"], data)
            except InternalServerError:
                result["error"] += 1
                continue
            result["created"] += 1

        return Response(json.dumps(result), status=201, content_type="application/json")

    def update(self, request: Request, **kwargs: dict) -> Response:
        """
        Viewpoint to update existing topics.
        """
        # TODO: Check permissions.
        data = request.json
        is_valid_update_topic(data)
        result = {"updated": 0, "error": 0}
        # for topic in data:
        #     id = topic.pop("id")
        #     rev = topic.pop("rev")
        #     url = "/".join((self.database_url, id))
        #     headers = self.database_headers
        #     headers["If-Match"] = rev
        #     response = requests.put(url, data=json.dumps(topic), headers=headers)
        #     if response.ok:
        #         result["updated"] += 1
        #     else:
        #         result["error"] += 1
        return Response(json.dumps(result), status=200, content_type="application/json")

    def delete(self, request: Request, **kwargs: dict) -> Response:
        """
        Viewpoint to delete existing topics.
        """
        return Response("Hello")


def get_get_rules_func(services: ServicesConfig) -> Callable[[Map], Iterable[Rule]]:
    """
    Contructor for Werkzeug's get_rules method.
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
