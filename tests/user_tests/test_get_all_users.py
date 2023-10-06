import random

from tests.static import Errors
from tests.user_tests.config import UserService


def test_get_all_users_successful():
    params = {
        "count": random.randint(0, 100)
    }
    r = UserService().get_all_users(params=params)

    assert r.status_code == 200
    assert len(r.json()["result"]) <= params["count"]
    for element in r.json()["result"]:
        assert len(element["email"]) > 0


def test_get_all_users_params_count_too_big():
    params = {
        "count": random.randint(999, 10000)
    }
    r = UserService().get_all_users(params=params)

    assert r.status_code == 200
    assert len(r.json()["result"]) <= params["count"]
    for element in r.json()["result"]:
        assert len(element["email"]) > 0


def test_get_all_users_wrong_params_count():
    params = {
        "count": -1
    }
    r = UserService().get_all_users(params=params)

    assert r.status_code == 400
    assert r.json() == Errors.wrong_count


def test_get_all_users_wrong_type_count():
    params = {
        "count": "!"
    }
    r = UserService().get_all_users(params=params)

    assert r.status_code == 400
    assert r.json() == Errors.count_not_number


def test_get_all_users_count_empty_string():
    params = {
        "count": ""
    }
    r = UserService().get_all_users(params=params)

    assert r.status_code == 400
    assert r.json() == Errors.count_not_number
