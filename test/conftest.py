import uuid

import pytest
from cryptography.fernet import Fernet
from app import app
from coding_files import connection_to_database, getting_request_data_and_cleaning_it
from flask import session





@pytest.fixture
def client():
    with app.test_client(allow_subdomain_redirects=True) as client:
        yield client


@pytest.fixture()
def runner(app):
    return app.test_cli_runner(allow_subdomain_redirects=True)


@pytest.fixture()
def mysql_connection():
    conn = connection_to_database.connection_to_mysql()
    yield conn


@pytest.fixture()
def student_client(client):
    with client.session_transaction() as session:
        app.config['SECRET_KEY'] = 'super secret key'
        session['session_id'] = unique_id = str(uuid.uuid4())
        key = Fernet.generate_key().decode("utf-8")
        session['key'] = key
        sql_insert_list = [session['session_id']]
        sql_insert_list.extend([getting_request_data_and_cleaning_it.encrypt_data("John", key),
                                getting_request_data_and_cleaning_it.encrypt_data("Toelkin", key),
                                getting_request_data_and_cleaning_it.encrypt_data("00000000", key),
                                getting_request_data_and_cleaning_it.encrypt_data("SkippySenior@yahoo.com", key),
                                getting_request_data_and_cleaning_it.encrypt_data("Student", key)])
        connection_to_database.insert_session(sql_insert_list)
        session['info_text'] = ""
        session.permanent = True
    yield client


@pytest.fixture()
def faculty_client(client):
    with client.session_transaction() as session:
        app.config['SECRET_KEY'] = 'super secret key'
        session['session_id'] = unique_id = str(uuid.uuid4())
        key = Fernet.generate_key().decode("utf-8")
        session['key'] = key
        sql_insert_list = [session['session_id']]
        sql_insert_list.extend([getting_request_data_and_cleaning_it.encrypt_data("Leovanne", key),
                                getting_request_data_and_cleaning_it.encrypt_data("Smith", key),
                                getting_request_data_and_cleaning_it.encrypt_data("22222222", key),
                                getting_request_data_and_cleaning_it.encrypt_data("SkippySenior@yahoo.com", key),
                                getting_request_data_and_cleaning_it.encrypt_data("Faculty", key)])
        connection_to_database.insert_session(sql_insert_list)
        session['info_text'] = ""
        session['course'] = ""
        session['admin'] = ""
        session['courses'] = ["TEST2020", "WAT4000"]
        session.permanent = True
    yield client


@pytest.fixture()
def admin_client(client):
    with client.session_transaction() as session:
        app.config['SECRET_KEY'] = 'super secret key'
        session['session_id'] = unique_id = str(uuid.uuid4())
        key = Fernet.generate_key().decode("utf-8")
        session['key'] = key
        sql_insert_list = [session['session_id']]
        sql_insert_list.extend([getting_request_data_and_cleaning_it.encrypt_data("Leovanne", key),
                                getting_request_data_and_cleaning_it.encrypt_data("Smith", key),
                                getting_request_data_and_cleaning_it.encrypt_data("22222222", key),
                                getting_request_data_and_cleaning_it.encrypt_data("SkippySenior@yahoo.com", key),
                                getting_request_data_and_cleaning_it.encrypt_data("Faculty", key)])
        connection_to_database.insert_session(sql_insert_list)
        session['info_text'] = ""
        session['course'] = ""
        session['admin'] = "Admin"
        session['courses'] = ["TEST2020", "WAT4000"]
        session.permanent = True
    yield client
