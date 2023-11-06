from tests.static import Errors, SuccessfulResponses
from tests.user_tests.config import UserService
from tests.user_tests.db_config import DBConnect


def _checks_400(r):
    assert r.status_code == 400
    assert r.json() == Errors.user_invalid_id


def test_get_user_info_successful(create_logged_in_user):
    headers = {
        "email": create_logged_in_user[0].json()["result"]["email"],
        "x-auth-token": create_logged_in_user[2]
    }
    r = UserService().get_user_info(user_id=create_logged_in_user[0].json()["result"]["id"], headers=headers)
    assert r.status_code == 200

    user_db_info = DBConnect().select_user_info_by_id(r.json()["result"]["id"])

    assert r.json()["result"]["id"] == create_logged_in_user[0].json()["result"]["id"]
    assert r.json()["result"]["email"] == user_db_info[0][2]
    assert r.json()["result"]["username"] == user_db_info[0][1]

    r = UserService().delete_a_user(user_id=create_logged_in_user[0].json()["result"]["id"])

    assert r.status_code == 200
    assert r.json() == SuccessfulResponses.deleted


def test_get_user_info_unsuccessful_user_empty(create_logged_in_user):
    headers = {
        "email": create_logged_in_user[0].json()["result"]["email"],
        "x-auth-token": create_logged_in_user[2]
    }
    r = UserService().get_user_info(user_id="", headers=headers)

    assert r.status_code == 404
