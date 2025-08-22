# automation-api-fakerestapi

Automation of FakerestAPI APIs with Python

## Test Cases

| ID    | Test Name                                     | Description                              | Input                                | Expected Result                         |
| ----- | --------------------------------------------- | ---------------------------------------- | ------------------------------------ | --------------------------------------- |
| TC001 | test_post_books_status_code_200               | Create a valid book                      | Valid JSON payload                   | Status 200, book created successfully   |
| TC002 | test_post_books_without_token_should_fail     | Attempt to create a book without a token | Valid JSON payload                   | Status 401 or 403, authentication error |
| TC003 | test_post_books_invalid_payload_returns_error | Create a book with invalid payload       | Payload with missing or wrong fields | Status 400/422, error in response body  |
| TC004 | test_post_books_invalid_header_returns_error  | Create a book with invalid header        | Invalid Content-Type header          | Status 415, Unsupported Media Type      |

##Report
Generate report.html using pytest -s --html=reports/report\_$(Get-Date -Format "yyyyMMdd_HHmmss").html
It is saved in \automation-api-python\reports
