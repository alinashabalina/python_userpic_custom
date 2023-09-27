import random
import string

import pytest

from tests.static import SuccessfulResponses
from tests.user_tests.config import UserService


@pytest.fixture(autouse=True)
def service_availability():
    service = UserService().check_service()
    if service.status_code != 200:
        raise Exception(f"Service is not available : status code {service.status_code}")
    else:
        pass


@pytest.fixture
def generate_email():
    email = ''.join(random.choices(string.ascii_lowercase, k=5)) + "@gmail.com"

    return email


@pytest.fixture
def generate_username():
    username = ''.join(random.choices(string.ascii_lowercase, k=5)) + ' ' + ''.join(
        random.choices(string.ascii_lowercase, k=5))

    return username


@pytest.fixture
def create_user_body(generate_email, generate_username):
    user = {}
    username = generate_username
    email = generate_email
    is_admin = random.choice([True, False])

    user["username"] = username
    user["email"] = email
    user["is_admin"] = is_admin

    return user


@pytest.fixture
def create_user(create_user_body):
    user = UserService().create_a_user(data=create_user_body)
    assert user.status_code == 201
    assert user.json()["message"] == SuccessfulResponses.created["message"]

    return user, create_user_body


@pytest.fixture
def create_group_body(create_user):
    group = {}
    user_id = create_user[0].json()["result"]["id"]
    group_name = ''.join(random.choices(string.ascii_lowercase, k=5))
    userpic_link = ''.join(random.choices(string.ascii_lowercase, k=5))
    is_default = random.choice([True, False])
    is_private = not is_default

    group["user_id"] = user_id
    group["group_name"] = group_name
    group["userpic_link"] = userpic_link
    group["is_default"] = is_default
    group["is_private"] = is_private

    return group, create_user[0].json()["result"]["id"]
