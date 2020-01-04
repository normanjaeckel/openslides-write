from typing import Dict, Type

from .base import Action
from .topic import TopicActionSet

action_sets = (TopicActionSet,)


def get_action_map() -> Dict[str, Type[Action]]:
    action_map = {}
    for action_set in action_sets:
        for action in action_set.actions:
            action_map[action.name] = action
    return action_map
