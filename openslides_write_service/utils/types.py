from typing import Any, Callable, Dict, Text

import redis
from mypy_extensions import TypedDict

ServicesConfig = TypedDict(
    "ServicesConfig", {"database": str, "sequencer": redis.Redis, "event_writer": str},
)

ApplicationConfig = TypedDict("ApplicationConfig", {"services": ServicesConfig})

StartResponse = Callable

WSGIEnvironment = Dict[Text, Any]
