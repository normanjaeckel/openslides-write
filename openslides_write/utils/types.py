from typing import Any, Callable, Dict, Text

from mypy_extensions import TypedDict

ApplicationConfig = TypedDict("ApplicationConfig", {"foo": str})

DBConfig = TypedDict(
    "DBConfig", {"protocol": str, "host": str, "port": int, "database": str}
)

StartResponse = Callable

WSGIEnvironment = Dict[Text, Any]
