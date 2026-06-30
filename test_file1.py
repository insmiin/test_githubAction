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

def test_username_not_empty(user,my_conftest_test):
    assert my_conftest_test == 'abcc', 'wrong value'
    assert user["username"], "username must not be empty"


def test_role_is_valid(user):
    valid_roles = {"admin", "editor", "viewer"}
    assert user["role"] in valid_roles, f"unexpected role: {user['role']}"


def test_admin_privilege(user):
    if user["role"] == "admin":
        assert user["username"] == "alice"   # only alice is admin in this set
    else:
        assert user["role"] in {"editor", "viewer"}