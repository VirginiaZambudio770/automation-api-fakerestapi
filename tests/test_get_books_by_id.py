import pytest
from api_client.books_api import BooksAPI
from config import config
from http import HTTPStatus
import requests

books_api = BooksAPI()

def test_get_books_status_code_200():
    #Verify happy path returns 200 OK
    response = books_api.get_book_by_id(1)
    assert response.status_code == 200, f"Expected status code 200 but got {response.status_code}. Response body: {response.text}"
    assert response.status_code == HTTPStatus.OK, f"Expected {HTTPStatus.OK} but got {response.status_code}"
    
    #  NEGATIVE TESTS 