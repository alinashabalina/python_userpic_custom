import random
import string

import pytest

from tests.user_tests.config import UserService


@pytest.fixture(autouse=True)
def service_availability():
    service = UserService().check_service()
    if service.status_code != 200:
        raise Exception(f"Service is not available : status code {service.status_code}")
    else:
        pass


@pytest.fixture
def create_user_body():
    user = {}
    username = ''.join(random.choices(string.ascii_lowercase, k=10))
    email = ''.join(random.choices(string.ascii_lowercase, k=5)) + "@gmail.com"
    is_admin = random.choice([True, False])

    user["username"] = username
    user["email"] = email
    user["is_admin"] = is_admin

    return user
