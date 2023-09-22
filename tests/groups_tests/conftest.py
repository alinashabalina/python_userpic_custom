import random
import string

import pytest

from tests.groups_tests.config import GroupService


class GroupFixtures:

    @pytest.fixture(autouse=True)
    def service_availability(self):
        service = GroupService().check_service()
        if service.status_code != 200:
            raise Exception(f"Service is not available : status code {service.status_code}")
        else:
            pass

    @pytest.fixture
    def create_group_body(self):
        group_body = {}
        user_id = 21
        group_name = ''.join(random.choices(string.ascii_lowercase, k=5))
        userpic_link = "https://picsopopop.com/p/OibkM9gsay5DQ1TQZ-RiGveNq4KFv-PxKwQ7AI0"

        group_body["user_id"] = user_id
        group_body["group_name"] = group_name
        group_body["userpic_link"] = userpic_link

        return group_body

