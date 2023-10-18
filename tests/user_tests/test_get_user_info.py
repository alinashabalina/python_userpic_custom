import pytest

from tests.user_tests.config import UserService
from tests.static import Errors, SuccessfulResponses
from tests.user_tests.db_config import DBConnect


def _checks_400(r):
    assert r.status_code == 400
    assert r.json() == Errors.user_invalid_id


def test_get_user_info_successful(create_user):
    r = UserService().get_user_info(user_id=create_user[0].json()["result"]["id"])

    user_db_info = DBConnect().select_user_info_by_id(r.json()["result"]["id"])

    assert r.status_code == 200
    assert r.json()["result"]["id"] == create_user[0].json()["result"]["id"]
    assert r.json()["result"]["email"] == user_db_info[0][2]
    assert r.json()["result"]["username"] == user_db_info[0][1]

    r = UserService().delete_a_user(user_id=create_user[0].json()["result"]["id"])

    assert r.status_code == 200
    assert r.json() == SuccessfulResponses.deleted


@pytest.mark.parametrize("user_id", ["0", None, False, " ", 999, "!"])
def test_get_user_info_unsuccessful_user_does_not_exist(user_id):
    r = UserService().get_user_info(user_id=user_id)

    _checks_400(r)


def test_get_user_info_unsuccessful_user_empty():
    r = UserService().get_user_info(user_id="")

    assert r.status_code == 404

