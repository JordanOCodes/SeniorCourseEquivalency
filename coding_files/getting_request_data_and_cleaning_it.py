import os
import uuid
from datetime import date
from werkzeug.utils import secure_filename
from werkzeug.security import generate_password_hash, check_password_hash
from cryptography.fernet import Fernet

ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg'}

request_attributes = ["RequestID", "TheDate",
                      "FirstName", "LastName", "UFID", "email",
                      "UFCourseID",
                      "FirstCourseID", "FirstCourseTitle", "FirstCredits", "FirstUniversity", "FirstDepartment",
                      "FirstTerm", "FirstGrade", "FirstInstructorEmail", "FirstTextbook", "FirstAuthor",
                      "IsSecondClass",
                      "SecondCourseID", "SecondCourseTitle", "SecondCredits", "SecondUniversity", "SecondDepartment",
                      "SecondTerm", "SecondGrade", "SecondInstructorEmail", "SecondTextbook", "SecondAuthor",
                      "TopicLoc1", "TopicLoc2", "TopicLoc3", "TopicLoc4", "TopicLoc5", "TopicLoc6", "TopicLoc7",
                      "TopicLoc8", "TopicLoc9", "TopicLoc10",
                      "TopicLoc11", "TopicLoc12", "TopicLoc13", "TopicLoc14", "TopicLoc15", "TopicLoc16", "TopicLoc17",
                      "TopicLoc18", "TopicLoc19", "TopicLoc20",
                      "AmountFirstFiles", "AmountSecondFiles", "OtherComments"
                      ]

course_attributes = [
    "CourseID", "CourseTitle", "Credits", "Department",
    "Topic1", "Topic2", "Topic3", "Topic4", "Topic5", "Topic6", "Topic7", "Topic8", "Topic9", "Topic10",
    "Topic11", "Topic12", "Topic13", "Topic14", "Topic15", "Topic16", "Topic17", "Topic18", "Topic19", "Topic20"
]


def class_args_to_list(form):
    course_info_list = [form["course_id"].upper().replace("", ""), form["course_title"], form["credits"], form["department"]]
    topics_list = [form["topic1"],
                   form["topic2"],
                   form["topic3"], form["topic4"], form["topic5"], form["topic6"],
                   form["topic7"],
                   form["topic8"], form["topic9"], form["topic10"], form["topic11"],
                   form["topic12"],
                   form["topic13"], form["topic14"], form["topic15"], form["topic16"],
                   form["topic17"],
                   form["topic18"], form["topic19"], form["topic20"]]

    temp_list = []
    for i in range(len(topics_list)):  # Create a list of topics, not including empty ""
        if topics_list[i] != "":
            temp_list.append(topics_list[i])
    for i in range(len(topics_list) - len(temp_list)):  # append "" to temp until you have 20 topics
        temp_list.append("")
    for i in range(len(temp_list)):  # append the topics to the course info list
        course_info_list.append(temp_list[i])

    return course_info_list


def insert_list_to_sql_tuple(insert_list):
    for i in range(len(insert_list)):
        if insert_list[i] == '':
            insert_list[i] = 'N/A'
    return tuple(insert_list)


def get_student_request_info_to_list(request, request_key, home_path):
    # First: double check files
    check_files_are_empty = check_if_files_are_empty(request)
    if check_files_are_empty != "Everything is all good":
        return check_files_are_empty

    sql_insert_list = []
    unique_id = str(uuid.uuid4())
    the_date = date.today().strftime("%Y%m%d")
    student_unique_id = the_date + "-" + unique_id
    sql_insert_list.extend([student_unique_id])

    sql_insert_list.extend([encrypt_data(request.form["first_name"], request_key),
                            encrypt_data(request.form["last_name"], request_key),
                            encrypt_data(request.form["ufid"], request_key),
                            encrypt_data(request.form["student_email"], request_key),
                            request.form["course_id"],
                            request.form["sub_course_id"], request.form["sub_course_title"],
                            request.form["sub_credits"], request.form["sub_university"],
                            request.form["sub_department"], request.form["sub_term"],
                            request.form["sub_grade"], request.form["sub_email"],
                            request.form["sub_textbook"], request.form["sub_author"]])

    if request.form.get('second_class'):
        sql_insert_list.append("1")
        sql_insert_list.extend([request.form["second_sub_course_id"], request.form["second_sub_course_title"],
                                request.form["second_sub_credits"], request.form["second_sub_university"],
                                request.form["second_sub_department"], request.form["second_sub_term"],
                                request.form["second_sub_grade"], request.form["second_sub_email"],
                                request.form["second_sub_textbook"], request.form["second_sub_author"]])
    else:
        sql_insert_list.append("0")
        sql_insert_list.extend(["N/A", "N/A",
                                "0", "N/A",
                                "N/A", "N/A",
                                "N/A", "N/A",
                                "N/A", "N/A"])

    for i in range(20):
        topic_str = ""
        for j in range(24):
            if request.form.get(str(i) + 'topic_file' + str(j)):
                topic_str += "1"
            else:
                topic_str += "0"
        sql_insert_list.append(topic_str)

    # File Stuff Now
    sql_insert_list.extend([request.form["AmountOfFirstClassFiles"], request.form["AmountOfSecondClassFiles"]])
    sql_insert_list.append(request.form['other_comments'])

    return sql_insert_list


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


# TODO ADD and allow_file() first what ALLOWED_EXTENSIONS...
def check_if_files_are_empty(request):
    if request.form.get('second_class'):
        if request.files['syllabus'].filename == '':
            return ["ERROR: Syllabus file for class one empty"]
        elif request.files['catalog'].filename == '':
            return ["ERROR: Catalog file for class one empty"]
        elif request.files['second_syllabus'].filename == '':
            return ["ERROR: Syllabus file for class two empty"]
        elif request.files['second_catalog'].filename == '':
            return ["ERROR: Catalog file for class two empty"]
    else:
        if request.files['syllabus'].filename == '':
            return ["ERROR: Syllabus file for empty"]
        elif request.files['catalog'].filename == '':
            return ["ERROR: Catalog file for empty"]
    return "Everything is all good"


def put_files_into_directory(request, request_id, home_path):
    file_slash = "/"
    if os.name == "nt":
        file_slash = "\\"

    course_path = home_path + file_slash + "static" + file_slash + "student_request_files" + file_slash + request.form["course_id"]
    student_path = course_path + file_slash + request_id
    course_path_exists = os.path.exists(course_path)
    if not course_path_exists:
        os.makedirs(course_path)

    all_files = [request.files['syllabus'], request.files['catalog']]
    f = request.files.getlist('file[]')
    for zipfile in f:
        if zipfile.filename == "":
            continue
        all_files.append(zipfile)

    if request.form.get('second_class'):
        all_files.extend([request.files['second_syllabus'], request.files['second_catalog']])
        f2 = request.files.getlist('second_file[]')
        for zipfile2 in f2:
            if zipfile2.filename == "":
                continue
            all_files.append(zipfile2)

    student_path_exists = os.path.exists(student_path)
    if not student_path_exists:
        os.makedirs(student_path)

    for i in range(len(all_files)):
        i_text = str(i)
        if i < 10:
            i_text = "0" + i_text
        filename = i_text + secure_filename(all_files[i].filename)
        all_files[i].save(os.path.join(student_path, filename))

    return ""


def remove_files_and_directory(request_id, uf_course_id, home_path):
    file_slash = "/"
    if os.name == "nt":
        file_slash = "\\"

    course_path = home_path + file_slash + "static" + file_slash + "student_request_files" + file_slash + uf_course_id
    student_path = course_path + file_slash + request_id
    files = os.listdir(student_path)
    for file in files:
        os.remove(student_path + file_slash + file)
    os.rmdir(student_path)
    return ""


def request_list_into_dict(request_list_row):
    """

    :param request_list_row: A list of string in the "request_attribute" order
    (The order that SQL sends it in)
    :return:
    """

    request_dict = {"Error": request_list_row[0], "key": request_list_row[1]}

    index = 2
    for attribute in request_attributes:
        request_dict[attribute] = request_list_row[index]
        index += 1
    topic_amount = 0
    for attribute in course_attributes:
        request_dict["UF" + attribute] = request_list_row[index]
        if len(attribute) > 5 and attribute[:5] == "Topic" and not request_list_row[index] in ['N/A', " ", ""]:
            topic_amount += 1
        index += 1
    request_dict["topic_amount"] = topic_amount

    # Decrypt information
    to_decrypt = ["FirstName", "LastName", "UFID", "email"]
    for element_name in to_decrypt:
        request_dict[element_name] = decode_data(request_dict[element_name], request_dict["key"])

    return request_dict


def course_list_to_dict(course_list):
    course_dict = {"Error": course_list[0]}
    index = 1
    for attribute in course_attributes:
        if course_list[index] == "N/A":
            course_dict[attribute] = ""
        else:
            course_dict[attribute] = course_list[index]
        index += 1
    topic_amount = 0
    return course_dict



def get_file_list(root_path, uf_course_id, request_id):
    file_path = root_path + "/static/student_request_files/" + uf_course_id + "/" + request_id + "/"
    return list(os.listdir(file_path))


def get_file_paths(file_list, request_dict, request_id):
    file_paths = []
    file_relative = "student_request_files/" + request_dict["UFCourseID"] + "/" + request_id + "/"
    index = 0
    for i in range(len(file_list)):
        file_paths.append(file_relative + file_list[i])
        index += 1
    for i in range(24 - index):
        file_paths.append("nothing.png")

    return file_paths


def get_post_request_info_to_list(request, request_key):
    sql_insert_list = []
    hashed_ufid = get_hashed_password(request.form["ufid"])
    sql_insert_list.extend([request.form["request_id"],
                            encrypt_data(request.form["first_name"], request_key),
                            encrypt_data(request.form["last_name"], request_key),
                            hashed_ufid,
                            encrypt_data(request.form["email"], request_key),
                            request.form["course_id"], request.form["course_title"], request.form["credits"],
                            request.form["department"],
                            request.form["sub_course_id"], request.form["sub_course_title"],
                            request.form["sub_credits"], request.form["sub_university"],
                            request.form["sub_term"], request.form["sub_grade"],
                            request.form["second_class"],
                            request.form["second_sub_course_id"], request.form["second_sub_course_title"],
                            request.form["second_sub_credits"], request.form["second_sub_university"],
                            request.form["second_sub_term"], request.form["second_sub_grade"],
                            request.form["faculty_comments"]])
    return sql_insert_list


def get_login_info_to_list(request, session_id, key):
    sql_insert_list = [session_id]
    sql_insert_list.extend([encrypt_data(request.form["first_name"], key),
                            encrypt_data(request.form["last_name"], key),
                            encrypt_data(request.form["ufid"], key),
                            encrypt_data(request.form["student_email"], key),
                            encrypt_data(request.form["authorization"], key)])
    return sql_insert_list


def encrypt_data(str_data, key_str):
    key = key_str.encode("utf-8")
    bit_data = str_data.encode("utf-8")
    cipher_suite = Fernet(key)
    cipher_bytes = cipher_suite.encrypt(bit_data)
    cipher_str = cipher_bytes.decode("utf-8")
    return cipher_str


def decode_data(cipher_string, key_str):
    key = key_str.encode("utf-8")
    cipher_bytes = cipher_string.encode("utf-8")
    cipher_suite = Fernet(key)
    bit_data = cipher_suite.decrypt(cipher_bytes)
    str_data = bit_data.decode("utf-8")
    return str_data


def get_hashed_password(plain_text_password):
    # Hash a password for the first time
    return generate_password_hash(plain_text_password)


def check_password(plain_text_password, hashed_password):
    # Check hashed password
    return check_password_hash(hashed_password, plain_text_password)


# if __name__ == '__main__':
#     text = "88123456"
#     hass = get_hashed_password(text)
#     no = check_password(text, hass)
#     print(no)
