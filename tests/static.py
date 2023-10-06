class Errors:
    user_invalid_id = {
        "message": "Enter a valid user_id",
    }

    user_not_in_the_database = {
        "message": "User does not exist in the database"
    }

    user_id_required = {
        "message": "Validation error: 'user_id' is a required property"
    }

    wrong_count = {
        "message": "Enter the correct count number"
    }

    count_not_number = {
        "message": "Count can only be a number"
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
