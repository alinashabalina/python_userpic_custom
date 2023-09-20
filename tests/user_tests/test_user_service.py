from tests.user_tests.config import UserService


def test_create_user_successful(create_user_body):
    r = UserService().create_a_user(data=create_user_body)
    assert r.status_code == 201
    assert r.json()["result"]["email"] == create_user_body["email"]
    assert r.json()["result"]["username"] == create_user_body["username"]
