"""
Main page deals with all the Flask application
"""
import datetime

from flask import Flask, session, render_template, request, redirect, url_for
from coding_files import create_html_text, connection_to_database, getting_request_data_and_cleaning_it, \
    preparing_to_connect_to_database, sending_email
import os
import uuid
from cryptography.fernet import Fernet
import sys
sys.path.insert(0, '/h/cnswww-course-equivalency-request.cise/course-equivalency-request.cise.ufl.edu/cgi-bin/env/Lib/site-packages')


app = Flask(__name__)
SESSION_TYPE = 'redis'
app.config.from_object(__name__)
app.config["SESSION_PERMANENT"] = True
app.config['SECRET_KEY'] = 'super secret key'


def establish_session(session_id, key):
    session['session_id'] = session_id
    session['key'] = key
    session['info_text'] = ""
    session.permanent = True
    app.permanent_session_lifetime = datetime.timedelta(minutes=20)


def get_authorization():
    if not is_current_session():
        return "NO AUTH"
    app.permanent_session_lifetime = datetime.timedelta(minutes=60)
    cipher_str = connection_to_database.get_session_authorization(session.get("session_id"))
    authorization_str = getting_request_data_and_cleaning_it.decode_data(cipher_str, session.get("key"))
    return authorization_str


@app.route('/renew_session_lifetime')
def renew_session_lifetime():
    if not is_current_session():
        return "False"
    app.permanent_session_lifetime = datetime.timedelta(minutes=60)
    return "True"


@app.route('/clear_session_lifetime')
def clear_session_lifetime():
    app.permanent_session_lifetime = datetime.timedelta(seconds=0)
    return "session time is zero seconds has been cleared"


def get_session_ufid():
    cipher_str = connection_to_database.get_session_ufid(session.get("session_id"))
    ufid_str = getting_request_data_and_cleaning_it.decode_data(cipher_str, session.get("key"))
    return ufid_str


def get_session_name_ufid_email_list():
    cipher_list = connection_to_database.get_session_name_ufid_email(session.get("session_id"))
    first_name = getting_request_data_and_cleaning_it.decode_data(cipher_list[0], session.get("key"))
    last_name = getting_request_data_and_cleaning_it.decode_data(cipher_list[1], session.get("key"))
    ufid = getting_request_data_and_cleaning_it.decode_data(cipher_list[2], session.get("key"))
    email = getting_request_data_and_cleaning_it.decode_data(cipher_list[3], session.get("key"))
    return [first_name, last_name, ufid, email]


def is_session_auth_student():
    authorization = get_authorization()
    if "Student" == authorization:
        return True
    return False


def is_session_auth_faculty():
    authorization = get_authorization()
    if "Faculty" == authorization:
        return True
    return False


def is_current_session():
    if session.get("session_id") and session.get("key"):
        return True
    return False


@app.route('/')
@app.route('/', methods=['POST'])
def login():
    if is_current_session():
        if is_session_auth_faculty():
            return redirect(url_for("faculty_root"))
        elif is_session_auth_student():
            return redirect(url_for("student_root"))
    else:
        session.clear()

    if request.method == 'POST':
        session_id = str(uuid.uuid4())
        key_str = Fernet.generate_key().decode("utf-8")
        insert_list = getting_request_data_and_cleaning_it.get_login_info_to_list(request, session_id, key_str)
        connection_to_database.insert_session(insert_list)
        establish_session(session_id, key_str)

        if True:  # if successful login
            authorization = request.form["authorization"]
            if authorization == "Student":
                session['courses'] = []
                session['admin'] = ""
                return redirect(url_for("student_root"))
            elif authorization == "Faculty":
                session['admin'] = request.form['admin']
                if session['admin'] == "Admin":
                    session['courses'] = connection_to_database.get_list_all_course_id()
                else:
                    session['courses'] = request.form.getlist('course')
                return redirect(url_for("faculty_root"))

    course_list = connection_to_database.get_list_all_sorted_course_ids_and_courses_faculty()

    return render_template("login.html", course_list=course_list)


@app.route('/faculty_root')
def faculty_root():
    if not is_session_auth_faculty():
        return redirect(url_for("login"))

    info_text = session['info_text']
    session['info_text'] = ""
    """
    This simply deals with the selection of pages for the faculty
    :return:
    """
    admin_privileges = ("Admin" == session['admin'])
    return render_template("faculty_root.html", info_text=info_text, admin_privileges=admin_privileges)


@app.route('/faculty_course_select')
@app.route('/faculty_course_select', methods=['POST', 'GET'])
def faculty_course_select():
    if not is_session_auth_faculty():
        return redirect(url_for("login"))
    """
    This is a page for faculty to select a course they wish to modify
    It's also a page that faculty will be sent back to after modifications
    :return:
    """
    # This deals with messages after modifications
    info_text = session['info_text']
    session['info_text'] = ""

    # If the course has been selected, or to add a new course
    if request.method == 'POST':
        the_course = request.form["course"]
        if "NEWCOURSE" == the_course:  # If new course
            return redirect(url_for("faculty_course_add"))
        else:  # else it's a course that already exist
            return redirect(url_for("faculty_course_modify", the_course=the_course))

    course_list = connection_to_database.get_list_all_sorted_course_ids_and_courses_faculty()
    return render_template("faculty_course_select.html", course_list=course_list, info_text=info_text)


@app.route('/faculty_course_modify')
@app.route('/faculty_course_modify', methods=['POST', 'GET'])
def faculty_course_modify():
    if not is_session_auth_faculty():
        return redirect(url_for("login"))
    """
    This page deals with modifying preexisting courses
    :return:
    """

    if request.method == 'POST':
        modified_course_info_list = getting_request_data_and_cleaning_it.class_args_to_list(request.form)
        session['info_text'] = connection_to_database.modify_course_row(modified_course_info_list)
        return redirect(url_for("faculty_root"))

    if not request.args.get("the_course"):
        session['info_text'] = "Error in choosing course to modify."
        return redirect(url_for("faculty_root"))

    the_course = request.args.get("the_course")
    course_info_list = connection_to_database.get_course_row(the_course)
    course_dict = getting_request_data_and_cleaning_it.course_list_to_dict(course_info_list)

    if course_dict["Error"] != "None":
        session['info_text'] = "Sorry, there was an error in retrieving the information. Please try again.\n" \
                               + course_info_list[0]
        return redirect(url_for("faculty_root"))

    course_info_list.pop(0)
    course_topics = [value for key, value in course_dict.items() if "Topic" == key[:5]]

    return render_template("faculty_course_modify.html", course_dict=course_dict, course_topics=course_topics)


@app.route('/faculty_course_add')
@app.route('/faculty_course_add', methods=['POST'])
def faculty_course_add():

    if not is_session_auth_faculty():
        return redirect(url_for("login"))
    error_message = ""
    if request.method == 'POST':
        if request.form["course_id"].upper().replace("",
                                                     "") in connection_to_database.get_list_all_course_id():  # If course is already in db
            session['info_text'] = request.form["course_id"].upper().replace("",
                                            "") + " is already in the database! Please try modifying it instead, or add a new course!"
        else:
            insert_list = getting_request_data_and_cleaning_it.class_args_to_list(request.form)
            session['info_text'] = connection_to_database.insert_course_row(insert_list)
            return redirect(url_for("faculty_root"))

    topic_html = create_html_text.html_add_course_topics()
    return render_template("faculty_course_add.html", topic_html=topic_html)


@app.route('/faculty_course_delete')
@app.route('/faculty_course_delete', methods=['POST', 'GET'])
def faculty_course_delete():
    if not is_session_auth_faculty() or not session['admin'] == "Admin":
        return redirect(url_for("login"))
    """
    This is a page for faculty to select a course they wish to modify
    It's also a page that faculty will be sent back to after modifications
    :return:
    """
    # If the course has been selected, or to add a new course
    if request.method == 'POST':
        the_course = request.form["course"]
        amount_request_for_course = connection_to_database.amount_request_in_a_course(the_course)
        if amount_request_for_course[0]:  # if request went through
            if amount_request_for_course[1] == 0:  # if there are no requests for the class
                session['info_text'] =  connection_to_database.remove_a_course(the_course)
            else:
                session['info_text'] = "Cannot Delete " + the_course + ", there are still " + str(
                    amount_request_for_course[1]) + " pending requests."
        else:
            session['info_text'] = amount_request_for_course[1]
        return redirect(url_for("faculty_root"))

    course_list = connection_to_database.get_list_all_sorted_course_ids_and_courses_faculty()
    return render_template("faculty_course_delete.html", course_list=course_list)


@app.route('/faculty_archived_select')
@app.route('/faculty_archived_select', methods=['POST', 'GET'])
def faculty_archived_select():
    if not is_session_auth_faculty():
        return redirect(url_for("login"))

    info_text = session['info_text']
    session['info_text'] = ""

    # If the course has been selected, or to add a new course
    if request.method == 'POST':
        ufid = request.form["ufid"]
        return redirect(url_for("faculty_archived_view", ufid=ufid))

    return render_template("faculty_archived_select.html", info_text=info_text)

@app.route('/faculty_archived_view')
@app.route('/faculty_archived_view', methods=['POST', 'GET'])
def faculty_archived_view():
    if not is_session_auth_faculty():
        return redirect(url_for("login"))
    info_text = session['info_text']
    session['info_text'] = ""
    if not request.args.get("ufid"):
        session['info_text'] = "Error in finding archived requests for that UFID."
        return redirect(url_for("faculty_archived_select"))

    student_ufid = request.args.get("ufid")
    list_of_requests = connection_to_database.get_list_archived_requests(student_ufid)

    if list_of_requests[0] != "None":
        session['info_text'] = list_of_requests[0]
        return redirect(url_for("faculty_archived_select"))
    elif len(list_of_requests) < 2:
        session['info_text'] = "Could not find the student UFID " + str(student_ufid) + " in our archive."
        return redirect(url_for("faculty_archived_select"))

    list_of_requests.pop(0) # Remove First element, so only request are here

    return render_template("faculty_archived_view.html", info_text=info_text, list_of_requests=list_of_requests,
                           amt_request=len(list_of_requests))


@app.route('/faculty_request_select')
@app.route('/faculty_request_select', methods=['POST', 'GET'])
def faculty_request_select():
    if not is_session_auth_faculty():
        return redirect(url_for("login"))
    info_text = session['info_text']
    session['info_text'] = ""

    if request.method == 'POST':
        request_id = request.form["request"]
        return redirect(url_for("faculty_review_request", request_id=request_id))

    list_of_allowed_courses = session['courses']
    list_of_requests = preparing_to_connect_to_database.get_all_request_for_all_allowed_courses(list_of_allowed_courses)
    if len(list_of_requests) == 0:
        info_text += "<br>You have no student course requests to review!!"
    html_request_select = create_html_text.html_list_of_request_select(list_of_requests)

    return render_template("faculty_request_select.html", html_request_select=html_request_select, info_text=info_text)


@app.route('/faculty_review_request')
@app.route('/faculty_review_request', methods=['POST', 'GET'])
def faculty_review_request():
    if not is_session_auth_faculty():
        return redirect(url_for("login"))
    root_path = os.path.dirname(__file__)
    if request.method == 'POST':

        request_status = request.form["ApprovedOrDenied"]
        request_key = Fernet.generate_key().decode("utf-8")
        insert_list = getting_request_data_and_cleaning_it.get_post_request_info_to_list(request, request_key)
        if request_status == "Approved":
            session['info_text'] += connection_to_database.insert_student_request_archive(insert_list, request_key) + "<br>"
            sending_email.student_request_approve(request.form['email'], request.form['first_name'],
                                                  request.form['last_name'], request.form['course_id'],
                                                  request.form['course_title'], request.form['faculty_comments'])

            session['info_text'] += connection_to_database.remove_row_from_student_request(request.form["request_id"],
                                                                                           request.form["course_id"],
                                                                                           root_path)
        elif request_status == "Denied":
            sending_email.student_request_denial(request.form['email'], request.form['first_name'],
                                                 request.form['last_name'], request.form['course_id'],
                                                 request.form['course_title'], request.form['faculty_comments'])
            session['info_text'] += connection_to_database.remove_row_from_student_request(request.form["request_id"],
                                                                                           request.form["course_id"],
                                                                                           root_path)
        return redirect(url_for("faculty_root"))

    if not request.args.get("request_id"):
        session['info_text'] = "Error in choosing course to modify."
        return redirect(url_for("faculty_root"))

    request_id = request.args.get('request_id')
    request_list = connection_to_database.get_request_and_course_row(request_id)
    request_dict = getting_request_data_and_cleaning_it.request_list_into_dict(request_list)
    file_list = getting_request_data_and_cleaning_it.get_file_list(root_path, request_dict["UFCourseID"], request_id)
    file_paths_list = getting_request_data_and_cleaning_it.get_file_paths(file_list, request_dict, request_id)
    course_topic_list = [value for key, value in request_dict.items() if "UFTopic" == key[:7]]
    course_topic_locations = [value for key, value in request_dict.items() if "TopicLoc" == key[:8]]
    html_tabs = create_html_text.html_tabs(file_list, request_dict)

    return render_template("faculty_review_request.html", request_dict=request_dict, root_path=root_path,
                           course_topic_list=course_topic_list, course_topic_locations=course_topic_locations,
                           html_tabs=html_tabs, file_paths_list=file_paths_list)


@app.route('/student_root')
@app.route('/student_root', methods=['POST'])
def student_root():
    if not is_session_auth_student():
        return redirect(url_for("login"))

    info_text = session['info_text']
    session['info_text'] = ""

    """
    This simply deals with the selection of pages for the student
    :return:
    """
    if request.method == 'POST':
        return redirect(url_for("student_course_select"))
    return render_template("student_root.html", info_text=info_text)


@app.route('/student_course_select')
@app.route('/student_course_select', methods=['POST', 'GET'])
def student_course_select():
    if not is_session_auth_student():
        return redirect(url_for("login"))

    info_text = session['info_text']
    session['info_text'] = ""

    if request.method == 'POST':
        the_course = request.form["course"]
        return redirect(url_for("student_course_equiv_form", the_course=the_course))

    course_list = connection_to_database.get_list_all_sorted_course_ids_and_courses_student()
    return render_template("student_course_select.html", course_list=course_list, info_text=info_text)


def check_if_user_already_has_request_in_database(the_course, session_ufid):
    have_request_pending = connection_to_database.check_if_already_in_all_requests_by_single_course(the_course,
                                                                                                    session_ufid)
    have_request_approved = connection_to_database.check_if_already_in_all_archive_by_single_course(the_course,
                                                                                                    session_ufid)
    if have_request_pending[0] and have_request_approved[0]:
        if have_request_pending[1]:
            return [False, "You already have a request pending for " + the_course]
        elif have_request_approved[1]:
            return [False, "You already have a request approved for " + the_course + "!"]
        else:
            return [True, "GOOD TO GO!"]
    else:
        return [False, "Error pulling data for " + the_course + ", please try again."]


@app.route('/student_course_equiv_form')
@app.route('/student_course_equiv_form', methods=['POST'])
def student_course_equiv_form():
    if not is_session_auth_student():
        return redirect(url_for("login"))

    if request.method == 'POST':
        root_path = os.path.dirname(__file__)
        request_key = Fernet.generate_key().decode("utf-8")
        insert_list = getting_request_data_and_cleaning_it.get_student_request_info_to_list(request, request_key,
                                                                                            root_path)

        check_if_use_can_make_request = check_if_user_already_has_request_in_database(request.form["course_id"],
                                                                                      get_session_ufid())
        if not check_if_use_can_make_request[0]:
            return redirect(url_for("student_root", text_after_add=check_if_use_can_make_request[1]))

        session['info_text'] = connection_to_database.insert_student_request_row(insert_list, request, request_key,
                                                                                 root_path)
        sending_email.student_request_confirmation(request.form['student_email'], request.form['first_name'],
                                                   request.form['last_name'], request.form['course_id'],
                                                   request.form['course_title'])
        return redirect(url_for("student_root"))

    if not request.args.get("the_course"):
        session['info_text'] = "Error in choosing course to modify."
        return redirect(url_for("student_root"))

    the_course = request.args.get("the_course")
    course_info_list = connection_to_database.get_course_row(the_course)
    if course_info_list[0] != "None":
        session['info_text'] = "Sorry, there was an error in retrieving the information. Please try again.\n"
        return redirect(url_for("student_course_select"))

    check_if_use_can_make_request = check_if_user_already_has_request_in_database(the_course, get_session_ufid())
    if not check_if_use_can_make_request[0]:
        session['info_text'] = check_if_use_can_make_request[1]
        return redirect(url_for("student_root"))

    course_info_list.pop(0)
    topic_html = create_html_text.html_topics(course_info_list[4:])
    list_of_topics_html = create_html_text.list_of_html_topics(course_info_list[4:])
    list_of_topics_visibility = create_html_text.list_of_html_topics_visibility(course_info_list[4:])

    return render_template("student_course_equiv_form.html", course_id=course_info_list[0],
                           course_title=course_info_list[1],
                           credits=course_info_list[2], department=course_info_list[3], topic_html=topic_html,
                           list_of_topics_html=list_of_topics_html, list_of_topics_visibility=list_of_topics_visibility,
                           session_info_list=get_session_name_ufid_email_list())


@app.route('/secret')
def secret():
    session.clear()
    return "<p>You've made it to the secret page!<br>" \
           "This was only made this for slight debugging purposes early on.<br>" \
           "I hope you enjoyed this little secret.</p>"


if __name__ == '__main__':
    app.run()
