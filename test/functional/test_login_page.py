def test_login_page_get_no_session(client):
    """
    GIVEN non user
    WHEN the '/' page is requested (GET)
    THEN check that the response is valid
    """
    response = client.get("/")
    assert response.status_code == 200


def test_get_faculty(faculty_client):
    """
    GIVEN a faculty user
    WHEN the '/' page is requested (GET)
    THEN check that the response is redirected 302, successfully 200, , to /faculty_root
    """

    response = faculty_client.get("/", follow_redirects=True)
    assert response.history[0].status_code == 302  # Immediately redirected
    assert response.status_code == 200  # We ultimately get to a page successfully
    assert response.request.path == "/faculty_root"  # as a faculty member we arrive at /faculty_root


def test_get_student(student_client):
    """
    GIVEN a faculty user
    WHEN the '/student_root' page is requested (GET)
    THEN check that the response is redirected 302, successfully 200, , to /student_root
    """
    response = student_client.get("/faculty_root", follow_redirects=True)
    assert response.history[0].status_code == 302  # Immediately redirected
    assert response.status_code == 200  # We ultimately get to a page successfully
    assert response.request.path == "/student_root"  # as a faculty member we arrive at /faculty_root
