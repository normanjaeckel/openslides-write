from typing import Any, Callable, Dict, Text

from mypy_extensions import TypedDict

ServicesConfig = TypedDict("ServicesConfig", {"database": str, "event_store": str},)

ApplicationConfig = TypedDict("ApplicationConfig", {"services": ServicesConfig})

StartResponse = Callable

WSGIEnvironment = Dict[Text, Any]
