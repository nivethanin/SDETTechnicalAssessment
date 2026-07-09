from concurrent.futures import ThreadPoolExecutor
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


@pytest.mark.load
def test_posts_endpoint_handles_small_parallel_request_burst(api_client):
    request_count = 5
    max_total_duration_seconds = 5.0
    max_average_duration_seconds = 1.5

    def fetch_posts():
        request_start = time.perf_counter()
        response = api_client.get(Endpoints.POSTS)
        request_duration = time.perf_counter() - request_start
        return response.status_code, request_duration

    burst_start = time.perf_counter()
    with ThreadPoolExecutor(max_workers=request_count) as executor:
        results = list(executor.map(lambda _: fetch_posts(), range(request_count)))
    total_duration_seconds = time.perf_counter() - burst_start

    status_codes = [status_code for status_code, _ in results]
    request_durations = [duration for _, duration in results]
    average_duration_seconds = sum(request_durations) / len(request_durations)

    logger.info(
        "Parallel burst finished in %.3fs with per-request durations: %s",
        total_duration_seconds,
        [round(duration, 3) for duration in request_durations],
    )

    assert all(status_code == 200 for status_code in status_codes)
    assert total_duration_seconds < max_total_duration_seconds, (
        f"Parallel burst took {total_duration_seconds:.3f}s, expected < {max_total_duration_seconds:.3f}s"
    )
    assert average_duration_seconds < max_average_duration_seconds, (
        f"Average request time was {average_duration_seconds:.3f}s, expected < {max_average_duration_seconds:.3f}s"
    )

