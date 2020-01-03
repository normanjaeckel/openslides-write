from typing import Iterable, Type

from ..utils.routing import RuleFactory
from .motion import MotionRuleFactory
from .topic import TopicRuleFactory


def get_rule_factories() -> Iterable[Type[RuleFactory]]:
    return (
        TopicRuleFactory,
        MotionRuleFactory,
    )
