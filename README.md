# SDET Technical Assessment - API Test Automation

## Overview

This project contains automated API tests for the public
[JSONPlaceholder](https://jsonplaceholder.typicode.com) service using Python and pytest


## Assumptions

- JSONPlaceholder is a mock API with non-persistent writes.
- `POST`, `PUT`, `PATCH`, and `DELETE` are expected to return successful status
	codes and echoed payloads, but no durable backend state is verified.
- Internet access is available when tests are executed.

## Scope Completed

Covered all main JSONPlaceholder resources:

- `/posts`
- `/comments`
- `/albums`
- `/photos`
- `/todos`
- `/users`

### Test Coverage Implemented

- Positive scenarios:
	- List retrieval for each resource
	- Single resource retrieval by ID
	- Basic query filtering per resource
- Response validations:
	- HTTP status code checks
	- JSON payload type/shape checks
	- Key field/value assertions
	- Nested object checks for `/users`
- Negative scenarios:
	- Non-existent IDs returning `404` and empty object responses
- Mutating operations (on `/posts`):
	- `POST` create
	- `PUT` full update
	- `PATCH` partial update
	- `DELETE` success response

## Project Structure

```
api/
	client.py        # API client wrapper around requests
	endpoints.py     # Route constants
tests/
	conftest.py      # Shared fixtures
	test_posts.py
	test_comments.py
	test_albums.py
	test_photos.py
	test_todos.py
	test_users.py
pytest.ini
requirements.txt
```

## Execution Instructions

### 1. Install dependencies

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### 2. Run the test suite

```bash
pytest
```

Optional verbose run:

```bash
pytest -v
```

Run only performance tests:

```bash
pytest -m performance -v
```

### 3. View test results

- Results are shown directly in terminal output.
- `pytest` summary includes total passed/failed tests and failure details.

## Coverage Summary

- Resources tested: `posts`, `comments`, `albums`, `photos`, `todos`, `users`
- Validation types:
	- status code verification
	- response body structure validation
	- content/value checks
	- query/filter behavior
	- negative path for invalid IDs
	- non-persistent CRUD-style behavior for `posts`

## TODOS

- Mutation negative tests
- Thorough schema validation via JSON schema library
- Data-driven full boundary matrix across all query parameters
- Network failure injection
- Performance/load testing
- Contract tests against versioned API specs