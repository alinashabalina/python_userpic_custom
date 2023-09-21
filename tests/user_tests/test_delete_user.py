import pytest

from tests.user_tests.config import UserService
from tests.user_tests.static import Errors, SuccessfulResponses


@pytest.mark.parametrize("user_id", ["user_id", "0", True, None, 999])
def test_delete_user_invalid_id(user_id):
    r = UserService().delete_a_user(user_id=user_id)

    assert r.status_code == 400
    assert r.json() == Errors.user_not_in_the_database


def test_delete_user_successful(create_user):
    r = UserService().delete_a_user(user_id=create_user[0].json()["result"]["id"])

    assert r.status_code == 200
    assert r.json() == SuccessfulResponses.deleted
