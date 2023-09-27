import random
import string

import pytest

from tests.groups_tests.config import GroupService


@pytest.fixture(autouse=True)
def service_availability():
    service = GroupService().check_service()
    if service.status_code != 200:
        raise Exception(f"Service is not available : status code {service.status_code}")
    else:
        pass
