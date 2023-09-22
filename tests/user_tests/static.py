class Errors:
    user_invalid_id = {
        "message": "Enter a valid user_id",
    }

    user_not_in_the_database = {
        "message": "User does not exist in the database"
    }


class SuccessfulResponses:
    deleted = {
        "message": "User successfully deleted"
    }

    created = {
        "message": "User created"
    }

    updated = {
        "message": "User successfully updated"
    }
