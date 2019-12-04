from typing import Any, Callable, Dict, Text

from mypy_extensions import TypedDict

DatabaseConfig = TypedDict(
    "DatabaseConfig", {"protocol": str, "host": str, "port": int}
)

ApplicationConfig = TypedDict("ApplicationConfig", {"database": DatabaseConfig},)

StartResponse = Callable

WSGIEnvironment = Dict[Text, Any]
