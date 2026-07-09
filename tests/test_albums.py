import pytest

from api.endpoints import Endpoints


def test_get_albums_returns_non_empty_list(api_client):
	response = api_client.get(Endpoints.ALBUMS)

	assert response.status_code == 200
	assert response.headers["Content-Type"].startswith("application/json")

	albums = response.json()
	assert isinstance(albums, list)
	assert len(albums) > 0
	assert isinstance(albums[0]["id"], int)
	assert isinstance(albums[0]["userId"], int)
	assert isinstance(albums[0]["title"], str)


def test_get_album_by_id_returns_expected_shape(api_client):
	response = api_client.get(f"{Endpoints.ALBUMS}/1")

	assert response.status_code == 200
	album = response.json()
	assert set(["userId", "id", "title"]).issubset(album.keys())
	assert album["id"] == 1
	assert isinstance(album["userId"], int)
	assert isinstance(album["title"], str)
	assert album["title"].strip() != ""


def test_get_albums_by_user_id_filter(api_client):
	response = api_client.get(f"{Endpoints.ALBUMS}?userId=1")

	assert response.status_code == 200
	albums = response.json()
	assert len(albums) > 0
	assert all(album["userId"] == 1 for album in albums)


@pytest.mark.parametrize("invalid_id", [0, -1, 999999])
def test_get_album_with_invalid_id_returns_not_found(api_client, invalid_id):
	response = api_client.get(f"{Endpoints.ALBUMS}/{invalid_id}")

	assert response.status_code == 404
	assert response.json() == {}
