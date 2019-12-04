import fastjsonschema  # type: ignore

from ..utils.schema import schema_version

is_valid_new_topic = fastjsonschema.compile(
    {
        "$schema": schema_version,
        "title": "New topics schema",
        "description": "An array of new topics.",
        "type": "array",
        "items": {
            "type": "object",
            "properties": {
                "title": {
                    "description": "A string. The title or headline of the topic.",
                    "type": "string",
                    "minLength": 1,
                },
                "text": {
                    "description": "A string containing HTML formatted text.",
                    "type": "string",
                },
                "attachments": {
                    "description": "An arry of attachment ids that should be referenced with this topic.",
                    "type": "array",
                    "items": {"type": "integer"},
                    "uniqueItems": True,
                },
            },
            "required": ["title"],
        },
        "minItems": 1,
        "uniqueItems": True,
    }
)


is_valid_update_topic = fastjsonschema.compile(
    {
        "$schema": schema_version,
        "title": "Update topics schema",
        "description": "An array of topics to be updated.",
        "type": "array",
        "items": {
            "type": "object",
            "properties": {
                "id": {
                    "description": "A string. The id of the topic.",
                    "type": "string",
                    # TODO: Add id validation.
                },
                "title": {
                    "description": "A string. The title or headline of the topic.",
                    "type": "string",
                    "minLength": 1,
                },
                "text": {
                    "description": "A string containing HTML formatted text.",
                    "type": "string",
                },
                "attachments": {
                    "description": "An arry of attachment ids that should be referenced with this topic.",
                    "type": "array",
                    "items": {"type": "integer"},
                    "uniqueItems": True,
                },
            },
            "required": ["id"],
        },
        "minItems": 1,
        "uniqueItems": True,
    }
)
