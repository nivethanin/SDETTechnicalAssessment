import pytest

from api.endpoints import Endpoints


def test_get_photos_returns_non_empty_list(api_client):
	response = api_client.get(Endpoints.PHOTOS)

	assert response.status_code == 200
	photos = response.json()
	assert isinstance(photos, list)
	assert len(photos) > 0
	assert isinstance(photos[0]["id"], int)
	assert isinstance(photos[0]["albumId"], int)
	assert photos[0]["url"].startswith("http")


def test_get_photo_by_id_returns_expected_shape(api_client):
	response = api_client.get(f"{Endpoints.PHOTOS}/1")

	assert response.status_code == 200
	photo = response.json()
	assert set(["albumId", "id", "title", "url", "thumbnailUrl"]).issubset(photo.keys())
	assert photo["id"] == 1
	assert isinstance(photo["albumId"], int)
	assert isinstance(photo["title"], str)
	assert photo["thumbnailUrl"].startswith("http")


def test_get_photos_by_album_id_filter(api_client):
	response = api_client.get(f"{Endpoints.PHOTOS}?albumId=1")

	assert response.status_code == 200
	photos = response.json()
	assert len(photos) > 0
	assert all(photo["albumId"] == 1 for photo in photos)


@pytest.mark.parametrize("invalid_id", [0, -1, 999999])
def test_get_photo_with_invalid_id_returns_not_found(api_client, invalid_id):
	response = api_client.get(f"{Endpoints.PHOTOS}/{invalid_id}")

	assert response.status_code == 404
	assert response.json() == {}
