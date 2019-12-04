from typing import Callable, Iterable

import requests
import simplejson as json
from werkzeug.exceptions import BadRequest
from werkzeug.routing import Map
from werkzeug.wrappers import Request, Response

from ..utils.routing import Rule
from ..utils.types import DBConfig
from .schema import is_valid_new_topic, is_valid_update_topic


class TopicViewSet:
    """
    Viewset for topics.

    During initialization we bind the viewpoint and database to the instance.
    """

    def __init__(self, viewpoint: str, db: DBConfig) -> None:
        self.viewpoint = viewpoint
        self.url = f"{db['protocol']}://{db['host']}:{db['port']}/{db['database']}"
        self.headers = {"Content-Type": "application/json"}

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
        # TODO: Check permissions.
        data = request.json
        is_valid_new_topic(data)
        result = {"created": 0, "error": 0}
        for topic in data:
            response = requests.post(
                self.url, data=json.dumps(topic), headers=self.headers
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
            url = "/".join((self.url, id))
            headers = self.headers
            headers["If-Match"] = rev
            response = requests.put(url, data=json.dumps(topic), headers=headers)
            print(response.text)
            if response.ok:
                result["updated"] += 1
            else:
                result["error"] += 1
        return Response(json.dumps(result), status=200, content_type="application/json")

    def delete(self, request: Request, **kwargs: dict) -> Response:
        """
        Viewpoint to delete existing topics.
        """
        return Response("Huhu3")


def get_get_rules_func(db: DBConfig) -> Callable[[Map], Iterable[Rule]]:
    """
    Contructor for get_rules method.
    """

    def get_rules(map: Map) -> Iterable[Rule]:
        """
        Rules for this app.
        """
        return [
            Rule(
                "/topics/new",
                endpoint="TopicViewSet new",
                methods=("POST",),
                view=TopicViewSet("new", db=db),
            ),
            Rule(
                "/topics/update",
                endpoint="TopicViewSet update",
                methods=("POST",),
                view=TopicViewSet("update", db=db),
            ),
            Rule(
                "/topics/delete",
                endpoint="TopicViewSet delete",
                methods=("POST",),
                view=TopicViewSet("delete", db=db),
            ),
        ]

    return get_rules
