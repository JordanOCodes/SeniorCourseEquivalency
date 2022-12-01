


def test_get_faculty_without_course(faculty_client):
    """
    GIVEN a faculty user
    WHEN the '/faculty_course_modify' page is requested WITHOUT a valid course(GET)
    THEN check that the response is redirect 302
    """
    response = faculty_client.get("/faculty_course_modify")
    assert response.status_code == 302


def test_get_faculty_with_course(faculty_client):
    """
    GIVEN a faculty user
    WHEN the '/faculty_course_modify' page is requested WITH a valid course(GET)
    THEN check that the response is valid 200
    """
    response = faculty_client.get("/faculty_course_modify?the_course=COP3502")
    assert response.status_code == 200
