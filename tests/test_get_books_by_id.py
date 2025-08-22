import pytest
from api_client.books_api import BooksAPI
from config import config
from datetime import datetime, timezone
from http import HTTPStatus
from tests.utils.book_helpers import assert_book_data_matches

books_api = BooksAPI()


def test_get_book_happy_path(existing_book):
    """ Verify happy path returns 200 OK """
    book_id = existing_book["id"]
    response = books_api.get_book_by_id(book_id)
    assert response.status_code == HTTPStatus.OK, f"Expected {HTTPStatus.OK} but got {response.status_code}"
    data = response.json()
    assert data["id"] == book_id

def test_get_book_content_type_json(existing_book):
    """ Verify Content-Type header is correct """
    book_id = existing_book["id"]
    response = books_api.get_book_by_id(book_id)
    assert response.headers["Content-Type"].startswith(config.HEADERS["Content-Type"].split("/")[0])

def test_get_book_returns_expected_data(existing_book):
    """ Verify returned data matches existing book """
    book_id = existing_book["id"]
    response = books_api.get_book_by_id(book_id)
    data = response.json()
    assert data["id"] == book_id
    assert "title" in data
    assert "description" in data
    assert "pageCount" in data

# NEGATIVE TESTS

def test_get_book_invalid_id(invalid_book_id):
    """ Verify invalid ID returns 400 Bad Request """
    response = books_api.get_book_by_id(invalid_book_id)
    assert response.status_code == HTTPStatus.BAD_REQUEST, f"Expected {HTTPStatus.BAD_REQUEST} but got {response.status_code}. Body: {response.text}"
    data = response.json()
    assert data.get("title") == "One or more validation errors occurred."

@pytest.mark.skip(reason="It is skipped because this API doesnt requiere token yet")  
def test_put_book_without_token(existing_book, valid_book_payload):
    """ Verify status code 401 or 403 without token """
    book_id = existing_book["id"]
    headers = {"Authorization": ""} # No Authorization
    response = books_api.get_book_by_id(book_id, headers=headers)
    assert response.status_code in (HTTPStatus.UNAUTHORIZED, HTTPStatus.FORBIDDEN)
    data = response.json()
    assert "errors" in data  