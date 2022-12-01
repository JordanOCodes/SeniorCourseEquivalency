

def test_get_student_redirects(student_client):
    """
    GIVEN a student user
    WHEN any non student page is requested (GET)
    THEN check that the response is redirected 302 successfully 200, to /student_root
    """

    response = student_client.get("/faculty_root", follow_redirects=True)
    assert response.history[0].status_code == 302 and response.status_code == 200 and response.request.path == "/student_root"

    response = student_client.get("/faculty_course_select", follow_redirects=True)
    assert response.history[0].status_code == 302 and response.status_code == 200 and response.request.path == "/student_root"

    response = student_client.get("/faculty_course_modify", follow_redirects=True)
    assert response.history[0].status_code == 302 and response.status_code == 200 and response.request.path == "/student_root"

    response = student_client.get("/faculty_course_delete", follow_redirects=True)
    assert response.history[0].status_code == 302 and response.status_code == 200 and response.request.path == "/student_root"

    response = student_client.get("/faculty_request_select", follow_redirects=True)
    assert response.history[0].status_code == 302 and response.status_code == 200 and response.request.path == "/student_root"

    response = student_client.get("/faculty_course_add", follow_redirects=True)
    assert response.history[0].status_code == 302 and response.status_code == 200 and response.request.path == "/student_root"

    response = student_client.get("/faculty_review_request", follow_redirects=True)
    assert response.history[0].status_code == 302 and response.status_code == 200 and response.request.path == "/student_root"


def test_get_faculty_redirects(faculty_client):
    """
    GIVEN a faculty user with no admin privilege
    WHEN any non faculty page is requested (GET)
    THEN check that the response is redirected 302 successfully 200, to /facultyt_root
    """
    response = faculty_client.get("/student_root", follow_redirects=True)
    assert response.history[0].status_code == 302 and response.status_code == 200 and response.request.path == "/faculty_root"

    response = faculty_client.get("/student_course_select", follow_redirects=True)
    assert response.history[0].status_code == 302 and response.status_code == 200 and response.request.path == "/faculty_root"

    response = faculty_client.get("/student_course_equiv_form", follow_redirects=True)
    assert response.history[0].status_code == 302 and response.status_code == 200 and response.request.path == "/faculty_root"

    response = faculty_client.get("/faculty_course_delete", follow_redirects=True)
    assert response.history[0].status_code == 302 and response.status_code == 200 and response.request.path == "/faculty_root"


def test_get_no_session_redirect(client):
    """
    GIVEN a non user
    WHEN any page other than "/" is requested (GET)
check that the response is redirected 302, successfully 200, to /
    """
    response = client.get("/faculty_root", follow_redirects=True)
    assert response.history[0].status_code == 302 and response.status_code == 200 and response.request.path == "/"

    response = client.get("/faculty_course_modify", follow_redirects=True)
    assert response.history[0].status_code == 302 and response.status_code == 200 and response.request.path == "/"

    response = client.get("/faculty_course_delete", follow_redirects=True)
    assert response.history[0].status_code == 302 and response.status_code == 200 and response.request.path == "/"

    response = client.get("/faculty_request_select", follow_redirects=True)
    assert response.history[0].status_code == 302 and response.status_code == 200 and response.request.path == "/"

    response = client.get("/faculty_course_add", follow_redirects=True)
    assert response.history[0].status_code == 302 and response.status_code == 200 and response.request.path == "/"

    response = client.get("/faculty_review_request", follow_redirects=True)
    assert response.history[0].status_code == 302 and response.status_code == 200 and response.request.path == "/"

    response = client.get("/student_root", follow_redirects=True)
    assert response.history[0].status_code == 302 and response.status_code == 200 and response.request.path == "/"

    response = client.get("/student_course_select", follow_redirects=True)
    assert response.history[0].status_code == 302 and response.status_code == 200 and response.request.path == "/"

    response = client.get("/student_course_equiv_form", follow_redirects=True)
    assert response.history[0].status_code == 302 and response.status_code == 200 and response.request.path == "/"

