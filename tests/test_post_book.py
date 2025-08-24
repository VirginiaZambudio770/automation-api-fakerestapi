import pytest
from api_client.books_api import BooksAPI
from config import config
from http import HTTPStatus
from tests.utils.book_helpers import assert_book_data_matches

books_api = BooksAPI()

def test_post_books_status_code_200(valid_book_payload):
    """ Verify happy path returns 200 OK """
    response = books_api.create_book(valid_book_payload)
    book_created = response.json()
    book_id = book_created["id"]
    assert response.status_code == HTTPStatus.OK, f"Expected {HTTPStatus.OK} but got {response.status_code}"
    
def test_post_books_content_type_json(valid_book_payload):
    """ Verify header Content-Type is equals to Content-Type from config file """
    response = books_api.create_book(valid_book_payload)
    assert response.headers["Content-Type"].startswith(config.HEADERS["Content-Type"].split("/")[0])

def test_post_books_returns_created_book_data(valid_book_payload):
    """ Verify expected data """
    response = books_api.create_book(valid_book_payload)
    data = response.json()
    assert "id" in data
    assert_book_data_matches(valid_book_payload, data)
    
def test_post_books_status_code_200(valid_book_payload):
    """ Verify happy path returns 200 OK """
    response = books_api.create_book(valid_book_payload)
    book_created = response.json()
    book_id = book_created["id"]
    assert response.status_code == HTTPStatus.OK, f"Expected {HTTPStatus.OK} but got {response.status_code}"
    
@pytest.mark.xfail(reason="API does not persist data, so GET after POST will fail")
def test_post_and_get_book_persists_data(valid_book_payload):
    """ Verify the post persists data """
    response = books_api.create_book(valid_book_payload)
    book_created = response.json()
    book_id = book_created["id"]
    get_response = books_api.get_book_by_id(book_id)
    assert get_response.status_code == HTTPStatus.OK, (
        f"Expected 200 OK but got {get_response.status_code}. Body: {get_response.text}"
    )
    book_retrieved = get_response.json()
    assert_book_data_matches(valid_book_payload, book_retrieved)
    
@pytest.mark.xfail(reason="API does not persist data, so GET after POST will fail")
def test_create_two_books_same_id(valid_book_payload):
    """ Verify behavior when creating two books with the same ID """
    response1 = books_api.create_book(valid_book_payload)
    book1 = response1.json()
    book_id = book1["id"]
    assert response1.status_code == HTTPStatus.OK, (
        f"Expected 200 OK but got {response1.status_code}. Body: {response1.text}"
    )
    second_payload = valid_book_payload.copy()
    second_payload["title"] = "Duplicate Book Test"
    second_payload["id"] = book_id
    response2 = books_api.create_book(second_payload)
    assert response2.status_code in [HTTPStatus.BAD_REQUEST, HTTPStatus.CREATED, HTTPStatus.OK], (
        f"Expected 400, 200 or 201 but got {response2.status_code}. Body: {response2.text}"
    )
    get_response = books_api.get_book_by_id(book_id)
    assert get_response.status_code == HTTPStatus.OK, (
        f"Expected 200 OK but got {get_response.status_code}. Body: {get_response.text}"
    )
    book_retrieved = get_response.json()
    assert book_retrieved["title"] == second_payload["title"]
   
#  NEGATIVE TESTS 

def test_post_books_invalid_payload_returns_error(invalid_book_payload):
    """ Verify that an invalid payload returns 400 Bad Request. """
    response = books_api.create_book(invalid_book_payload)
    assert response.status_code == 400 
    data = response.json()
    assert "errors" in data 
    
def test_post_books_invalid_header_returns_error(invalid_book_payload):
    """ Verify that an invalid content-type returns 415 Unsupported Media Type. """
    headers = {"Content-Type": "1111"}
    response = books_api.create_book(invalid_book_payload, headers=headers)
    assert response.status_code == 415
    data = response.json()
    assert data.get("title") == "Unsupported Media Type"
        
@pytest.mark.xfail(reason="API does not require authentication") 
def test_post_books_without_token_should_fail(valid_book_payload):
    """ Verify that it returns 401 UNAUTHORIZED or 403 FORBIDDEN """
    headers = {"Authorization": ""}  # No Authorization
    response = books_api.create_book(valid_book_payload, headers=headers)  
    assert response.status_code in (HTTPStatus.UNAUTHORIZED, HTTPStatus.FORBIDDEN), (
        f"Expected 401 or 403 but got {response.status_code}. Body: {response.text}"
    )
    data = response.json()
    assert "errors" in data 