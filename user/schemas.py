class ValidationSchemas:
    UserCreateSchema = {
        "type": "object",
        "properties": {
            "username": {
                "type": "string"
            },
            "email": {
                "type": "string"
            },
            "is_admin": {
                "type": "boolean"
            },
        },
        "required": ["username", "email", "is_admin"],
        "additionalProperties": False,
    }
