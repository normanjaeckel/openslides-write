from typing import Iterable, Type

from .base import Action
from .topic import TopicActionSet

action_sets = (TopicActionSet,)


def get_actions() -> Iterable[Type[Action]]:
    for action_set in action_sets:
        yield from action_set.actions
