from typing import Any

from werkzeug.routing import Rule as WerkzeugRule


class Rule(WerkzeugRule):
    """
    Customized Rule to bind view function to the rule.
    """

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        self.view = kwargs.pop("view")
        super().__init__(*args, **kwargs)
