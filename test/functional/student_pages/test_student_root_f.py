
def test_get_student(student_client):
    """
    GIVEN a student user
    WHEN the '/student_root' page is requested (GET)
    THEN check that the response is valid
    """

    response = student_client.get("/student_root")
    assert response.status_code == 200

