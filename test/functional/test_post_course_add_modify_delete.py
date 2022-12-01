import pytest
from flask import session
from coding_files import connection_to_database


def test_add_course(faculty_client):
    """
    GIVEN a faculty member and that TEST2020 is NOT in the Course database
    WHEN a request is made to add a class on /faculty_course_add (POST) with VALID request data
    THEN check that the session['info_text'] is properly updated and that the course is in the database
    """
    the_data = {'course_id': 'TEST2020', 'course_title': 'The Test Course!', 'credits': '3', 'department': 'NOT CISE',
         'topic1': 'Happy', 'topic2': 'We Are New', 'topic3': 'Nueva', 'topic4': '', 'topic5': '',
         'topic6': '', 'topic7': '', 'topic8': '', 'topic9': '', 'topic10': '', 'topic11': '',
         'topic12': '', 'topic13': '', 'topic14': '', 'topic15': '', 'topic16': '', 'topic17': '',
         'topic18': '', 'topic19': '', 'topic20': '', 'submit_button': 'Submit New Course'}
    response = faculty_client.post("/faculty_course_add", data=the_data)
    print("Did you change the text that returns in connection_to_database.insert_course_row??")
    assert session["info_text"] == "TEST2020 has been successfully added to the database of courses!"
    assert connection_to_database.get_course_row("TEST2020")[1] == "TEST2020"


def test_add_course_already_added(faculty_client):
    """
    GIVEN a faculty member and that TEST2020 is ALREADY in the Course database
    WHEN a request is made to add a class on /faculty_course_add (POST) with VALID request data
    THEN check that the session['info_text'] is updated properly and that the course is in the database
    """
    the_data = {'course_id': 'TEST2020', 'course_title': 'The Test Course!', 'credits': '3',
                'department': 'NOT CISE',
                'topic1': 'Happy', 'topic2': 'We Are New', 'topic3': 'Nueva', 'topic4': '', 'topic5': '',
                'topic6': '', 'topic7': '', 'topic8': '', 'topic9': '', 'topic10': '', 'topic11': '',
                'topic12': '', 'topic13': '', 'topic14': '', 'topic15': '', 'topic16': '', 'topic17': '',
                'topic18': '', 'topic19': '', 'topic20': '', 'submit_button': 'Submit New Course'}
    response = faculty_client.post("/faculty_course_add", data=the_data)
    print("Did you change the text that returns in connection_to_database.insert_course_row??")
    assert session["info_text"] == "TEST2020 is already in the database! Please try modifying it instead, or add a new course!"
    assert connection_to_database.get_course_row("TEST2020")[1] == "TEST2020"


def test_add_course_missing_info(faculty_client):
    """
    GIVEN a faculty member and that TEST2021 is NOT ALREADY in the Course database
    WHEN a request is made to add a class on /faculty_course_add (POST) with INVALID request data, missing title and credits
    THEN check that the course is not properly added into the datbase
    """
    the_data = {'course_id': 'TEST2021',
                'department': 'NOT CISE',
                'topic1': 'Happy', 'topic2': 'We Are New', 'topic3': 'Nueva', 'topic4': '', 'topic5': '',
                'topic6': '', 'topic7': '', 'topic8': '', 'topic9': '', 'topic10': '', 'topic11': '',
                'topic12': '', 'topic13': '', 'topic14': '', 'topic15': '', 'topic16': '', 'topic17': '',
                'topic18': '', 'topic19': '', 'topic20': '', 'submit_button': 'Submit New Course'}
    response = faculty_client.post("/faculty_course_add", data=the_data)
    print("Did you change the text that returns in connection_to_database.insert_course_row??")
    assert connection_to_database.get_course_row("TEST2021") == ['None']



def test_modify_course(faculty_client):
    """
    GIVEN a faculty member and that TEST2020 is in the Course database
    WHEN a request is made to add a class on /faculty_course_modify (POST) with VALID request data
    THEN check that the session['info_text'] is properly updated and that the course's topic has been modified in the database
    """
    the_data = {'course_id': 'TEST2020', 'course_title': 'The Test Course!', 'credits': '3', 'department': 'NOT CISE',
         'topic1': 'Sad', 'topic2': 'We Are New', 'topic3': 'Nueva', 'topic4': '', 'topic5': '',
         'topic6': '', 'topic7': '', 'topic8': '', 'topic9': '', 'topic10': '', 'topic11': '',
         'topic12': '', 'topic13': '', 'topic14': '', 'topic15': '', 'topic16': '', 'topic17': '',
         'topic18': '', 'topic19': '', 'topic20': '', 'submit_button': 'Submit New Course'}
    response = faculty_client.post("/faculty_course_modify", data=the_data)
    print("Did you change the text that returns in connection_to_database.insert_course_row??")
    assert session["info_text"] == "TEST2020 has been successfully been modified in the database!"
    assert connection_to_database.get_course_row("TEST2020")[5] == "Sad"


def test_delete_course(admin_client):
    """
    GIVEN an admin member and that TEST2020 is in the Course database
    WHEN a request is made to add a class on /faculty_course_delete (POST) with VALID request data
    THEN check that the session['info_text'] is properly updated and that the course is NOT in the database
    """
    the_data = {'course': 'TEST2020'}

    assert connection_to_database.get_course_row("TEST2020")[1] == "TEST2020"
    response = admin_client.post("/faculty_course_delete", data=the_data)
    assert session['info_text'] == "Course TEST2020 has been successfully removed from the course database"
    assert len(connection_to_database.get_course_row("TEST2020")) == 1 # Only Error

