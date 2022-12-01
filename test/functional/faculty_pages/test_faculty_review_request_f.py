
def test_get_faculty_no_request(faculty_client):
    """
    GIVEN a faculty user
    WHEN the '/faculty_request_select' page is requested (GET)
    THEN check that the response is valid
    """
    response = faculty_client.get("/faculty_review_request")
    assert response.status_code == 302