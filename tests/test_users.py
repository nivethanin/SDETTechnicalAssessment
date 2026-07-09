import pytest

from api.endpoints import Endpoints


def test_get_users_returns_non_empty_list(api_client):
	response = api_client.get(Endpoints.USERS)

	assert response.status_code == 200
	users = response.json()
	assert isinstance(users, list)
	assert len(users) > 0
	assert isinstance(users[0]["id"], int)
	assert isinstance(users[0]["email"], str)
	assert isinstance(users[0]["address"], dict)


def test_get_user_by_id_returns_expected_shape(api_client):
	response = api_client.get(f"{Endpoints.USERS}/1")

	assert response.status_code == 200
	user = response.json()
	required_keys = [
		"id", "name", "username", "email", "address", "phone", "website", "company"
	]

	assert set(required_keys).issubset(user.keys())
	assert user["id"] == 1
	assert isinstance(user["name"], str)
	assert isinstance(user["username"], str)
	assert "@" in user["email"]
	assert set(["street", "suite", "city", "zipcode", "geo"]).issubset(user["address"].keys())
	assert set(["name", "catchPhrase", "bs"]).issubset(user["company"].keys())


def test_get_users_by_username_filter(api_client):
	response = api_client.get(f"{Endpoints.USERS}?username=Bret")

	assert response.status_code == 200
	users = response.json()
	assert len(users) == 1
	assert users[0]["username"] == "Bret"


@pytest.mark.parametrize("invalid_id", [0, -1, 999999])
def test_get_user_with_invalid_id_returns_not_found(api_client, invalid_id):
	response = api_client.get(f"{Endpoints.USERS}/{invalid_id}")

	assert response.status_code == 404
	assert response.json() == {}
