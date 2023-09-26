from tests.user_tests.config import UserService


def test_create_group(create_group_body):
    r = UserService().create_a_group(data=create_group_body[0])

    assert r.status_code == 201
    assert r.json()["result"]["group_name"] == create_group_body[0]["group_name"]
    assert r.json()["result"]["user_id"] == create_group_body[1]
    assert r.json()["result"]["userpic_link"] == create_group_body[0]["userpic_link"]
