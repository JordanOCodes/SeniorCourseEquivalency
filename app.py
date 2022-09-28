from flask import Flask, render_template, request, redirect, url_for
from coding_files import create_html_text, connection_to_database, declutter_main_page

app = Flask(__name__)


@app.route('/')
def hello_world():
    return 'Hello World!'


@app.route('/faculty_root')
def faculty_root():
    return render_template("faculty_root.html")


@app.route('/faculty_course_select')
@app.route('/faculty_course_select', methods=['POST', 'GET'])
def faculty_course_select():
    if not request.args.get("text_after_add"):
        text_after_add = ""
    else:
        text_after_add = request.args.get('text_after_add')
    if request.method == 'POST':
        the_course = request.form["course"]
        if "NEWCOURSE" == the_course:
            return redirect(url_for("faculty_course_add"))
        else:
            return redirect(url_for("faculty_course_modify", the_course=the_course))

    course_select = create_html_text.html_list_of_courses()
    return render_template("faculty_course_select.html", course_select=course_select, text_after_add=text_after_add)


@app.route('/faculty_course_modify')
@app.route('/faculty_course_modify', methods=['POST', 'GET'])
def faculty_course_modify():
    if not request.args.get("the_course"):
        text_after_add = "Error in choosing course to modify."
        return redirect(url_for("faculty_course_select", text_after_add=text_after_add))
    the_course = request.args.get("the_course")
    course_info_list = connection_to_database.get_course_row(the_course)
    if course_info_list[0] != "None":
        error_message = "Sorry, there was an error in retrieving the information. Please try again.\n" \
                        + course_info_list[0]
        return redirect(url_for("faculty_course_select", text_after_add=error_message))

    course_info_list.pop(0)
    attribute_html = create_html_text.html_modify_course_attributes(course_info_list[4:])

    if request.method == 'POST':
        modified_course_info_list = declutter_main_page.class_args_to_list(request.form)
        text_after_modify = connection_to_database.modify_course_row(modified_course_info_list)
        return redirect(url_for("faculty_course_select", text_after_add=text_after_modify))
    #TODO This will be for when you want a check, add last
    """ 
        return redirect(url_for("faculty_course_modify_check", course_info_list=course_info_list,
                                modified_course_info_list=modified_course_info_list))
    """

    return render_template("faculty_course_modify.html", course_id=course_info_list[0], course_title=course_info_list[1],
                           credits=course_info_list[2], department=course_info_list[3], attribute_html=attribute_html)


@app.route('/faculty_course_add')
@app.route('/faculty_course_add', methods=['POST'])
def faculty_course_add():

    error_message = ""
    if request.method == 'POST':
        if request.form["course_id"] in connection_to_database.get_list_all_course_id(): # If course is already in db
            error_message = "Course " + request.form["course_id"] + " is already in the database! Please try " \
                                                                        "modifying it instead, or add a new course! "
        else:
            insert_list = declutter_main_page.class_args_to_list(request.form)
            text_after_add = connection_to_database.insert_course_row(insert_list)
            return redirect(url_for("faculty_course_select", text_after_add=text_after_add))



    attribute_html = create_html_text.html_add_course_attributes()
    return render_template("faculty_course_add.html", attribute_html=attribute_html, error_message=error_message)


@app.route('/student_course_select')
@app.route('/student_course_select', methods=['POST', 'GET'])
def student_course_select():
    if not request.args.get("error_message"):
        error_message = ""
    else:
        error_message = request.args.get('error_message')
    if request.method == 'POST':
        the_course = request.form["course"]
        return redirect(url_for("course_equiv_student_form", the_course=the_course))

    course_select = create_html_text.html_list_of_courses()
    return render_template("student_course_select.html", course_select=course_select, error_message=error_message)


@app.route('/course_equiv_student_form')
def course_equiv_student_form():
    if not request.args.get("the_course"):
        error_message = "Error in choosing course to modify."
        return redirect(url_for("student_course_select", error_message=error_message))
    the_course = request.args.get("the_course")
    course_info_list = connection_to_database.get_course_row(the_course)
    if course_info_list[0] != "None":
        error_message = "Sorry, there was an error in retrieving the information. Please try again.\n"
        return redirect(url_for("student_course_select", text_after_add=error_message))

    course_info_list.pop(0)
    attribute_html = create_html_text.html_checkbox_attributes(course_info_list[4:])

    return render_template("course_equiv_student_form.html", course_id=course_info_list[0], course_title=course_info_list[1],
                           credits=course_info_list[2], department=course_info_list[3], attribute_html=attribute_html)

if __name__ == '__main__':
    app.run()
