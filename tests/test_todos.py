import pytest

from api.endpoints import Endpoints


def test_get_todos_returns_non_empty_list(api_client):
	response = api_client.get(Endpoints.TODOS)

	assert response.status_code == 200
	todos = response.json()
	assert isinstance(todos, list)
	assert len(todos) > 0
	assert isinstance(todos[0]["id"], int)
	assert isinstance(todos[0]["title"], str)
	assert isinstance(todos[0]["completed"], bool)


def test_get_todo_by_id_returns_expected_shape(api_client):
	response = api_client.get(f"{Endpoints.TODOS}/1")

	assert response.status_code == 200
	todo = response.json()
	assert set(["userId", "id", "title", "completed"]).issubset(todo.keys())
	assert todo["id"] == 1
	assert isinstance(todo["userId"], int)
	assert isinstance(todo["title"], str)
	assert isinstance(todo["completed"], bool)


def test_get_todos_by_completed_filter(api_client):
	response = api_client.get(f"{Endpoints.TODOS}?completed=true")

	assert response.status_code == 200
	todos = response.json()
	assert len(todos) > 0
	assert all(todo["completed"] is True for todo in todos)


@pytest.mark.parametrize("invalid_id", [0, -1, 999999])
def test_get_todo_with_invalid_id_returns_not_found(api_client, invalid_id):
	response = api_client.get(f"{Endpoints.TODOS}/{invalid_id}")

	assert response.status_code == 404
	assert response.json() == {}
