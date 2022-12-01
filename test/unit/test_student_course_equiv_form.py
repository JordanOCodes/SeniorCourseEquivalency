
def test_first_name(student_client):
    """
    GIVEN a Flask application configured for testing
    WHEN the '/' page is requested (GET)
    THEN check that the response is valid
    """
    response = student_client.get("/student_root") # TODO CHANGE

    assert response.status_code == 200