from copy import deepcopy

from tests.user_tests.config import UserService


def test_create_user_successful(create_user_body):
    r = UserService().create_a_user(data=create_user_body)
    assert r.status_code == 201
    assert r.json()["result"]["email"] == create_user_body["email"]
    assert r.json()["result"]["username"] == create_user_body["username"]


def test_create_user_unsuccessful_field_missing(create_user_body):
    items = ["username", "email", "is_admin"]
    for item in items:
        data = deepcopy(create_user_body)
        data.pop(item)
        r = UserService().create_a_user(data=data)
        assert r.status_code == 400
        assert item in r.json()["message"]
