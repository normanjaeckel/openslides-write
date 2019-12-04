from typing import Any, Callable, Dict, Text

from mypy_extensions import TypedDict

ServiceConfig = TypedDict("ServiceConfig", {"protocol": str, "host": str, "port": int})

ServicesConfig = TypedDict(
    "ServicesConfig",
    {"database": ServiceConfig, "get_id": ServiceConfig, "writer": ServiceConfig},
)

ApplicationConfig = TypedDict("ApplicationConfig", {"services": ServicesConfig},)

StartResponse = Callable

WSGIEnvironment = Dict[Text, Any]
