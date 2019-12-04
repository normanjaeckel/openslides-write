from typing import Iterable

from werkzeug.routing import Map, RuleFactory

from ..utils.routing import Rule
from ..utils.types import DBConfig
from .views import get_get_rules_func


class Topics(RuleFactory):
    """
    App for simple topics that can be shown in agenda.

    During initialization we bind the get_rules method from apps's views.
    """

    def __init__(self, db: DBConfig) -> None:
        self.get_rules_func = get_get_rules_func(db)

    def get_rules(self, map: Map) -> Iterable[Rule]:
        """
        """
        return self.get_rules_func(map)
