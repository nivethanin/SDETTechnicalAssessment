import logging
import time
import pytest
from api.endpoints import Endpoints

logger = logging.getLogger(__name__)


@pytest.mark.performance
@pytest.mark.parametrize(
    "endpoint,max_duration_seconds",
    [
        (Endpoints.POSTS, 3.0),
        (Endpoints.USERS, 3.0),
    ],
)
def test_list_endpoints_respond_within_threshold(api_client, endpoint, max_duration_seconds):
    start_time = time.perf_counter()
    response = api_client.get(endpoint)
    duration_seconds = time.perf_counter() - start_time
    logger.info("%s took %.3fs to respond", endpoint, duration_seconds)

    assert response.status_code == 200
    assert duration_seconds < max_duration_seconds, (
        f"{endpoint} took {duration_seconds}s, expected < {max_duration_seconds}s"
    )
