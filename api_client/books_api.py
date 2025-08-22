import requests
from config import config

class BooksAPI:

    ENDPOINT = config.BOOKS_ENDPOINT

    def get_books(self, headers=None):
        if headers is None:
            headers = config.HEADERS
        return requests.get(f"{config.BASE_URL}{self.ENDPOINT}", headers=headers)

    def get_book_by_id(self, book_id, headers=None):
        if headers is None:
            headers = config.HEADERS
        return requests.get(f"{config.BASE_URL}{self.ENDPOINT}/{book_id}", headers=headers)

    def create_book(self, payload, headers=None):
        if headers is None:
            headers = config.HEADERS
        return requests.post(f"{config.BASE_URL}{self.ENDPOINT}",json=payload, headers=headers)
    
    def update_book(self, book_id, payload, headers=None):
        if headers is None:
            headers = config.HEADERS
        return requests.put(f"{config.BASE_URL}{self.ENDPOINT}/{book_id}",json=payload, headers=headers)
    
    def delete_book(self, book_id, headers=None):
        if headers is None:
            headers = config.HEADERS
        return requests.delete(f"{config.BASE_URL}{self.ENDPOINT}/{book_id}", headers=headers)
