from copy import deepcopy

from tests.user_tests.config import UserService
from tests.user_tests.static import SuccessfulResponses


def _checks_400(r):
    assert r.status_code == 400
    assert "Validation error" in r.json()["message"]


def test_update_user_successful(create_user, generate_email, generate_username):
    data = create_user[1]
    data["username"] = generate_username
    data["email"] = generate_email
    data['is_admin'] = False
    r = UserService().update_a_user(data=data, user_id=create_user[0].json()["result"]["id"])

    assert r.status_code == 200
    assert r.json()["message"] == SuccessfulResponses.updated["message"]
    assert r.json()["result"]["email"] == generate_email
    assert r.json()["result"]["username"] == generate_username
    assert r.json()["result"]["id"] == create_user[0].json()["result"]["id"]

    r = UserService().delete_a_user(user_id=create_user[0].json()["result"]["id"])

    assert r.status_code == 200
    assert r.json() == SuccessfulResponses.deleted


def test_update_user_unsuccessful_empty_body(create_user):
    r = UserService().update_a_user(data={}, user_id=create_user[0].json()["result"]["id"])

    _checks_400(r)


def test_update_user_unsuccessful_field_missing(create_user):
    data = deepcopy(create_user[1])
    data.pop("username")
    r = UserService().update_a_user(data=data, user_id=create_user[0].json()["result"]["id"])

    _checks_400(r)


def test_update_user_unsuccessful_wrong_data_type(create_user):
    data = deepcopy(create_user[1])
    data["username"] = 1
    r1 = UserService().update_a_user(data=data, user_id=create_user[0].json()["result"]["id"])

    data = deepcopy(create_user[1])
    data["is_admin"] = "opop"
    r2 = UserService().create_a_user(data=data)

    data = deepcopy(create_user[1])
    data["email"] = True
    r3 = UserService().create_a_user(data=data)

    for r in [r1, r2, r3]:
        _checks_400(r)
