class ValidationSchemas:
    GroupCreateSchema = {
        "type": "object",
        "properties": {
            "user_id": {
                "type": "integer"
            },
            "group_name": {
                "type": "string"
            },
            "userpic_link": {
                "type": "string"
            },
            "is_default": {
                "type": "boolean"
            },
            "is_private": {
                "type": "boolean"
            }
        },
        "required": ["user_id", "group_name", "userpic_link", "is_default", "is_private"],
        "additionalProperties": False,
    }
