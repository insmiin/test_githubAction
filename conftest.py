import pytest

@pytest.fixture(scope="session")
def my_conftest_test():
    return 'abc'