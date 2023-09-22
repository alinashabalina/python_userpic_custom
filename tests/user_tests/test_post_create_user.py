from copy import deepcopy

from tests.user_tests.config import UserService


def _checks_400(r):
    assert r.status_code == 400
    assert "Validation error" in r.json()["message"]


def test_create_user_successful(create_user):
    assert create_user[0].json()["result"]["email"] == create_user[1]["email"]
    assert create_user[0].json()["result"]["username"] == create_user[1]["username"]


def test_create_user_unsuccessful_field_missing(create_user_body):
    data = deepcopy(create_user_body)
    data.pop("username")
    r = UserService().create_a_user(data=data)

    _checks_400(r)


def test_create_user_unsuccessful_empty_body():
    r = UserService().create_a_user(data={})

    _checks_400(r)


def test_create_user_unsuccessful_wrong_data_type(create_user_body):
    data = deepcopy(create_user_body)
    data["username"] = 1
    r1 = UserService().create_a_user(data=data)

    data = deepcopy(create_user_body)
    data["is_admin"] = "opop"
    r2 = UserService().create_a_user(data=data)

    data = deepcopy(create_user_body)
    data["email"] = True
    r3 = UserService().create_a_user(data=data)

    for r in [r1, r2, r3]:
        _checks_400(r)
