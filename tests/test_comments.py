import pytest

from api.endpoints import Endpoints


def test_get_comments_returns_non_empty_list(api_client):
	response = api_client.get(Endpoints.COMMENTS)

	assert response.status_code == 200
	comments = response.json()
	assert isinstance(comments, list)
	assert len(comments) > 0
	assert isinstance(comments[0]["id"], int)
	assert isinstance(comments[0]["postId"], int)
	assert isinstance(comments[0]["email"], str)


def test_get_comment_by_id_returns_expected_shape(api_client):
	response = api_client.get(f"{Endpoints.COMMENTS}/1")

	assert response.status_code == 200
	comment = response.json()
	assert set(["postId", "id", "name", "email", "body"]).issubset(comment.keys())
	assert comment["id"] == 1
	assert isinstance(comment["postId"], int)
	assert isinstance(comment["name"], str)
	assert "@" in comment["email"]
	assert isinstance(comment["body"], str)


def test_get_comments_by_post_id_filter(api_client):
	response = api_client.get(f"{Endpoints.COMMENTS}?postId=1")

	assert response.status_code == 200
	comments = response.json()
	assert len(comments) > 0
	assert all(comment["postId"] == 1 for comment in comments)


@pytest.mark.parametrize("invalid_id", [0, -1, 999999])
def test_get_comment_with_invalid_id_returns_not_found(api_client, invalid_id):
	response = api_client.get(f"{Endpoints.COMMENTS}/{invalid_id}")

	assert response.status_code == 404
	assert response.json() == {}
