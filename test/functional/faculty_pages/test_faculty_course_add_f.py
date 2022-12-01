from coding_files import connection_to_database

def test_get_faculty(faculty_client):
    """
    GIVEN a faculty user
    WHEN the '/faculty_course_add' page is requested (GET)
    THEN check that the response is valid
    """

    response = faculty_client.get("/faculty_course_add")
    assert response.status_code == 200

