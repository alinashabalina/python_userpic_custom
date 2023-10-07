import random

from tests.static import Errors
from tests.user_tests.config import UserService


def test_get_all_users_successful_no_limit_no_offset():
    r = UserService().get_all_users(params={})

    assert r.status_code == 200
    for element in r.json()["result"]:
        assert len(element["email"]) > 0


def test_get_all_users_params_limit_too_big():
    params = {
        "limit": random.randint(999, 10000)
    }
    r = UserService().get_all_users(params=params)

    assert r.status_code == 200
    assert len(r.json()["result"]) <= params["limit"]
    for element in r.json()["result"]:
        assert len(element["email"]) > 0


def test_get_all_users_wrong_params_limit():
    params = {
        "limit": -1
    }
    r = UserService().get_all_users(params=params)

    assert r.status_code == 400
    assert r.json() == Errors.wrong_count


def test_get_all_users_wrong_type_limit():
    params = {
        "limit": "!"
    }
    r = UserService().get_all_users(params=params)

    assert r.status_code == 400
    assert r.json() == Errors.count_not_number


def test_get_all_users_limit_empty_string():
    params = {
        "limit": ""
    }
    r = UserService().get_all_users(params=params)

    assert r.status_code == 400
    assert r.json() == Errors.count_not_number


def test_get_all_users_successful_limited():
    params = {
        "limit": random.randint(0, 50)
    }
    r = UserService().get_all_users(params=params)

    assert r.status_code == 200
    assert len(r.json()["result"]) <= params["limit"]
    for element in r.json()["result"]:
        assert len(element["email"]) > 0


def test_get_all_users_successful_limited_with_offset():
    params = {
        "limit": 50,
        "offset": 5
    }
    r = UserService().get_all_users(params=params)

    assert r.status_code == 200
    assert len(r.json()["result"]) <= params["limit"]
    assert r.json()["result"][0]["id"] == 6
    for element in r.json()["result"]:
        assert len(element["email"]) > 0


def test_get_all_users_wrong_params_offset():
    params = {
        "offset": -1
    }
    r = UserService().get_all_users(params=params)

    assert r.status_code == 400
    assert r.json() == Errors.wrong_count


def test_get_all_users_wrong_params_offset_and_limit():
    params = {
        "offset": -1,
        "limit": 1.5
    }
    r = UserService().get_all_users(params=params)

    assert r.status_code == 400
    assert r.json() == Errors.count_not_number


def test_get_all_users_wrong_type_params_offset_and_limit():
    params = {
        "offset": "",
        "limit": "!"
    }
    r = UserService().get_all_users(params=params)

    assert r.status_code == 400
    assert r.json() == Errors.count_not_number


def test_get_all_users_successful_offset_more_than_limit():
    params = {
        "limit": 50,
        "offset": 60
    }
    r = UserService().get_all_users(params=params)

    assert r.status_code == 200
    assert len(r.json()["result"]) == 0
