from ..base import ActionSet
from .actions import TopicCreate


class TopicActionSet(ActionSet):
    """
    Action set for simple topics that can be shown in agenda.
    """

    actions = (TopicCreate,)
