from . import fields
from .base import Model


class Topic(Model):
    id = fields.IdField(description="A string. The id of the topic.")
    title = fields.CharField(
        description="A string. The title or headline of the topic."
    )
    text = fields.TextField(description="A string containing HTML formatted text.")
    attachments = fields.ManyToManyArrayField(
        description="An array of attachment ids that should be referenced with this topic."
    )
