import random
import string

import pytest

from tests.user_tests.config import UserService
from tests.user_tests.static import SuccessfulResponses


class UserFixtures:
    @pytest.fixture(autouse=True)
    def service_availability(self):
        service = UserService().check_service()
        if service.status_code != 200:
            raise Exception(f"Service is not available : status code {service.status_code}")
        else:
            pass


    @pytest.fixture
    def generate_email(self):
        email = ''.join(random.choices(string.ascii_lowercase, k=5)) + "@gmail.com"

        return email


    @pytest.fixture
    def generate_username(self):
        username = ''.join(random.choices(string.ascii_lowercase, k=5)) + ' ' + ''.join(
            random.choices(string.ascii_lowercase, k=5))

        return username


    @pytest.fixture
    def create_user_body(self, generate_email, generate_username):
        user = {}
        username = generate_username
        email = generate_email
        is_admin = random.choice([True, False])

        user["username"] = username
        user["email"] = email
        user["is_admin"] = is_admin

        return user


    @pytest.fixture
    def create_user(self, create_user_body):
        user = UserService().create_a_user(data=create_user_body)
        assert user.status_code == 201
        assert user.json()["message"] == SuccessfulResponses.created["message"]

        return user, create_user_body
