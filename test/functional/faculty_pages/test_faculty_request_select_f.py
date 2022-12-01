
def test_get_faculty(faculty_client):
    """
    GIVEN a faculty user
    WHEN the '/faculty_request_select' page is requested (GET)
    THEN check that the response is valid
    """
    response = faculty_client.get("/faculty_request_select")
    print(response.data)
    assert response.status_code == 200
