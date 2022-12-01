def test_get_student_no_course(student_client):
    """
    GIVEN a student user
    WHEN the '/student_course_equiv_form' page is requested WITHOUT a course (GET)
    THEN check that the response is redirect 302
    """

    response = student_client.get("/student_course_equiv_form")
    assert response.status_code == 302


def test_get_student_with_course(student_client):
    """
    GIVEN a student user
    WHEN the '/student_course_equiv_form' page is requested WITH a valid course(GET)
    THEN check that the response is valid
    """

    response = student_client.get("/student_course_equiv_form?the_course=COP3502")
    assert response.status_code == 200

