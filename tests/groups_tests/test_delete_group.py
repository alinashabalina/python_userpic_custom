def test_delete_group_successful():
    r = GroupService().delete_a_group(group_id=2)

    assert r.status_code == 204


def test_delete_group_unsuccessful():
    r = GroupService().delete_a_group(group_id="1345676782")

    assert r.status_code == 400


def test_delete_group_unsuccessful():
    r = GroupService().delete_a_group(group_id=False)

    assert r.status_code == 400