import pytest
from api.client import APIClient


@pytest.fixture(scope="session")
def api_client():
    """
    Shared API client used across all tests.
    Created once per test session so it doesn't need
    to be re-created for each test.
    """
    return APIClient()