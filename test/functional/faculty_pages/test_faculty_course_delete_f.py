

def test_get_faculty_with_admin(admin_client):
    """
    GIVEN a faculty user
    WHEN the '/faculty_course_delete' page is requested WITHOUT a valid admin (GET)
    THEN check that the response is redirect 302
    """
    response = admin_client.get("/faculty_course_delete")
    assert response.status_code == 200

