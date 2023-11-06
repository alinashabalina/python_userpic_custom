import random
import string

import pytest

from tests.static import SuccessfulResponses
from tests.user_tests.config import UserService
from tests.user_tests.db_config import DBConnect


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
def generate_password():
    password="password" + str(random.randint(1, 10000) + 1)
    return password


@pytest.fixture
def create_user_body(generate_email, generate_username, generate_password):
    user = {}
    username = generate_username
    email = generate_email
    is_admin = random.choice([True, False])

    user["username"] = username
    user["email"] = email
    user["is_admin"] = is_admin
    user["password"] = generate_password

    return user


@pytest.fixture
def create_user(create_user_body):
    user = UserService().create_a_user(data=create_user_body)
    assert user.status_code == 201
    assert user.json()["message"] == SuccessfulResponses.created["message"]

    return user, create_user_body


@pytest.fixture
def create_admin(create_user_body):
    create_user_body["is_admin"] = True

    user = UserService().create_a_user(data=create_user_body)

    assert user.status_code == 201
    assert user.json()["message"] == SuccessfulResponses.created["message"]

    return user, create_user_body


@pytest.fixture
def create_logged_in_user(create_user_body):
    user = UserService().create_a_user(data=create_user_body)
    assert user.status_code == 201
    assert user.json()["message"] == SuccessfulResponses.created["message"]

    email = user.json()["result"]["email"]
    password = user.json()["result"]["password"]

    data = {
        "email": email,
        "password": password
    }

    login = UserService().user_login(data=data)
    assert login.status_code == 200

    token = DBConnect().select_user_info_by_id(user_id=user.json()["result"]["id"])[0][5]

    return user, create_user_body, token


@pytest.fixture
def create_logged_in_admin(create_user_body):
    create_user_body["is_admin"] = True

    user = UserService().create_a_user(data=create_user_body)

    assert user.status_code == 201
    assert user.json()["message"] == SuccessfulResponses.created["message"]

    email = user.json()["result"]["email"]
    password = user.json()["result"]["password"]

    data = {
        "email": email,
        "password": password
    }

    login = UserService().admin_login(data=data)
    assert login.status_code == 200

    token = DBConnect().select_user_info_by_id(user_id=user.json()["result"]["id"])[0][5]

    return user, create_user_body, token


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
