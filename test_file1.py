from logging import exception

import pytest

# ── Parameterised fixture ──────────────────────────────────────────────────────

@pytest.fixture(params=[
    {"username": "alice", "role": "admin"},
    {"username": "bob",   "role": "editor"},
    {"username": "xxab", "role": "viewer"},
])
def user(request):
    """Yields one user dict per parameter set."""
    return request.param


# ── Tests that consume the fixture ────────────────────────────────────────────

def test_username_not_empty(user,my_conftest_conntest):
    try:
        mycursor = my_conftest_conntest.cursor(dictionary=True)
        mysql_query = "SELECT sportID FROM GB_Qat.sports where sportID !=0"
        mycursor.execute(mysql_query)
        data = mycursor.fetchall()  # [{'sportID': 1}, {'sportID': 2}, {'sportID': 3}]
        my_conftest_conntest.commit()  # Ends the transaction
        all_sportIDs_dict = [sport['sportID'] for sport in data]  # [1, 2, 3, 4,....,67]
    except exception():
        pytest.fail(f"MySQL getMemHitHistory_Mysql query error: {err}")
    finally:
        if mycursor:
            mycursor.close()
    assert user["username"], "username must not be empty"
    assert all_sportIDs_dict == [1], "wronggggg"


def test_role_is_valid(user):
    valid_roles = {"admin", "editor", "viewer"}
    assert user["role"] in valid_roles, f"unexpected role: {user['role']}"


def test_admin_privilege(user):
    if user["role"] == "admin":
        assert user["username"] == "alice"   # only alice is admin in this set
    else:
        assert user["role"] in {"editor", "viewer"}