def assert_book_data_matches(payload, response_data):
    assert response_data["title"] == payload["title"]
    assert response_data["description"] == payload["description"]
    assert response_data["pageCount"] == payload["pageCount"]
    assert response_data["excerpt"] == payload["excerpt"]
    assert response_data["publishDate"].split("T")[0] == payload["publishDate"].split("T")[0]
