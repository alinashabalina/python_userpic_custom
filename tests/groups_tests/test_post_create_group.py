from copy import deepcopy

from tests.groups_tests.config import GroupService
from tests.static import Errors

from tests.user_tests.conftest import create_group_body, \
    create_user, create_user_body, generate_username, generate_email


def _checks_400(r):
    assert r.status_code == 400
    assert "Validation error" in r.json()["message"]


def test_create_group_successful(create_group_body):
    r = GroupService().create_a_group(data=create_group_body[0])

    assert r.status_code == 201
    assert r.json()["result"]["user_id"] == create_group_body[1]
    assert r.json()["result"]["userpic_link"] == create_group_body[0]["userpic_link"]


def test_create_group_unsuccessful_missing_field(create_group_body):
    data = create_group_body[0]
    data.pop("user_id")
    r = GroupService().create_a_group(data=data)

    assert r.status_code == 400#
    assert r.json() == Errors.user_id_required


def test_create_group_unsuccessful_wrong_data_type(create_group_body):
    data = deepcopy(create_group_body[0])
    data["username"] = 1
    r1 = GroupService().create_a_group(data=data)

    data = deepcopy(create_group_body[0])
    data["is_admin"] = "opop"
    r2 = GroupService().create_a_group(data=data)

    data = deepcopy(create_group_body[0])
    data["email"] = True
    r3 = GroupService().create_a_group(data=data)

    for r in [r1, r2, r3]:
        _checks_400(r)