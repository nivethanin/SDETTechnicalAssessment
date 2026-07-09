import pytest

from api.endpoints import Endpoints


def test_get_posts_returns_non_empty_list(api_client):
	response = api_client.get(Endpoints.POSTS)

	assert response.status_code == 200
	posts = response.json()
	assert isinstance(posts, list)
	assert len(posts) > 0
	assert isinstance(posts[0]["id"], int)
	assert isinstance(posts[0]["userId"], int)
	assert isinstance(posts[0]["title"], str)


def test_get_post_by_id_returns_expected_shape(api_client):
	response = api_client.get(f"{Endpoints.POSTS}/1")

	assert response.status_code == 200
	post = response.json()
	assert set(["userId", "id", "title", "body"]).issubset(post.keys())
	assert post["id"] == 1
	assert isinstance(post["userId"], int)
	assert isinstance(post["title"], str)
	assert isinstance(post["body"], str)


def test_get_posts_by_user_id_filter(api_client):
	response = api_client.get(f"{Endpoints.POSTS}?userId=1")

	assert response.status_code == 200
	posts = response.json()
	assert len(posts) > 0
	assert all(post["userId"] == 1 for post in posts)


def test_create_post_returns_created_with_id(api_client):
	payload = {
		"userId": 1,
		"title": "SDET assessment post",
		"body": "Created during API automation exercise"
	}

	response = api_client.post(Endpoints.POSTS, json=payload)

	assert response.status_code == 201
	created_post = response.json()
	assert created_post["title"] == payload["title"]
	assert created_post["body"] == payload["body"]
	assert created_post["userId"] == payload["userId"]
	assert "id" in created_post
	assert isinstance(created_post["id"], int)


def test_update_post_with_put_returns_full_updated_resource(api_client):
	payload = {
		"id": 1,
		"userId": 1,
		"title": "Updated title",
		"body": "Updated body"
	}

	response = api_client.put(f"{Endpoints.POSTS}/1", json=payload)

	assert response.status_code == 200
	updated_post = response.json()
	assert updated_post == payload
	assert isinstance(updated_post["id"], int)


def test_update_post_with_patch_returns_partially_updated_resource(api_client):
	payload = {"title": "Patched title"}

	response = api_client.patch(f"{Endpoints.POSTS}/1", json=payload)

	assert response.status_code == 200
	patched_post = response.json()
	assert patched_post["title"] == payload["title"]


def test_delete_post_returns_success_status(api_client):
	response = api_client.delete(f"{Endpoints.POSTS}/1")

	assert response.status_code == 200


@pytest.mark.parametrize("invalid_id", [0, -1, 999999])
def test_get_post_with_invalid_id_returns_not_found(api_client, invalid_id):
	response = api_client.get(f"{Endpoints.POSTS}/{invalid_id}")

	assert response.status_code == 404
	assert response.json() == {}
