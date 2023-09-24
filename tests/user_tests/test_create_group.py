from tests.user_tests.config import UserService


def test_create_group():
    data = {
        "user_id": "21",
        "group_name": "group",
        "userpic_link": "https://picsopopop.com/p/OibkM9gsay5DQ1TQZ-RiGveNq4KFv-PxKwQ7AI0"
    }
    r = UserService().create_a_group(data=data)
    assert r.status_code == 201
    # something is wrong with the user service not with the test