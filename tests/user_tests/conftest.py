import random
import string

import pytest


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
