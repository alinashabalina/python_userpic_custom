from copy import deepcopy

from tests.groups_tests.config import GroupService
from tests.user_tests.conftest import UserFixtures as u
from tests.groups_tests.conftest import GroupFixtures as g


def test_create_group_successful():
    print(u.create_user[0])
    r = GroupService().create_a_group(data=g.create_group_body)
    print(r.json())
