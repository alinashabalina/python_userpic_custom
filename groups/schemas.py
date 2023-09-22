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
        },
        "required": ["user_id", "group_name", "userpic_link"],
        "additionalProperties": False,
    }
