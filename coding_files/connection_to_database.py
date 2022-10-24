"""
This file deals with connecting to the mysql database
"""

import mysql.connector
from mysql.connector import errorcode
from coding_files import preparing_to_connect_to_database, getting_request_data_and_cleaning_it
import os


def connection_to_mysql(is_online=False):
    """
    This will connect to the mysql database using the parameters stated below
    Be careful!!! Must return connection object "cnx"
        Afterwards, save the returned object then create a cursor object.
    :param is_online:
    :return: mysql connection object
    """
    if is_online:
        print("online")
        config = {
            'user': 'joldham1',
            'password': 'CISECourse1234',
            'host': 'mysql.cise.ufl.edu',
            'port': '3306',
            'database': 'CourseEquivalency',
            'raise_on_warnings': True
        }
    else:
        config = {
            'user': 'root',
            'password': 'root',
            'host': '127.0.0.1',
            'port': '3306',
            'database': 'courseequivalency',
            'raise_on_warnings': True
        }

    try:
        cnx = mysql.connector.connect(**config)
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Something is wrong with your user name or password")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("Database does not exist")
        else:
            print(err)
    else:
        return cnx


def get_list_all_course_id():
    """
    This functions gets a list of every course id from the course table
    :return: a list of every course id
    """
    try:
        my_db = connection_to_mysql()
        my_cursor = my_db.cursor(prepared=True)
        my_cursor.execute("""SELECT CourseID FROM Course""")

        course_id_array = []
        for course in my_cursor:
            course_id_array.append(course[0])
        my_cursor.close()
        my_db.close()
        return course_id_array
    except mysql.connector.Error as error:
        return ["parameterized query failed {}".format(error)]


def get_list_all_sorted_course_ids_and_courses_faculty():
    """

    :return: A list of [[courseID0, courseTitle0, WordsAboutIFFinished0], [courseID1, courseTitle1, Words1]...]
    """
    try:
        my_db = connection_to_mysql()
        my_cursor = my_db.cursor(prepared=True)
        my_cursor.execute("""SELECT CourseID, CourseTitle, Topic1 
                             FROM Course
                             ORDER BY CourseID ASC""")
        courses = []
        for course in my_cursor:
            course = list(course)
            if course[2] != "N/A":
                course[2] = ""
            courses.append(course)
        my_cursor.close()
        my_db.close()
        courses.sort()
        return courses
    except mysql.connector.Error as error:
        return "parameterized query failed {}".format(error)


def get_list_all_sorted_course_ids_and_courses_student():
    """

    :return: A list of [[courseID0, courseTitle0, [courseID1, courseTitle1...]
    """
    try:
        my_db = connection_to_mysql()
        my_cursor = my_db.cursor(prepared=True)
        my_cursor.execute("""SELECT CourseID, CourseTitle  FROM Course
                             WHERE Topic1 != 'N/A'
                             ORDER BY CourseID ASC""")
        courses = []
        for course in my_cursor:
            courses.append(list(course))
        my_cursor.close()
        my_db.close()
        courses.sort()
        return courses
    except mysql.connector.Error as error:
        return "parameterized query failed {}".format(error)


def insert_course_row(insert_list):
    try:
        my_db = connection_to_mysql()
        my_cursor = my_db.cursor(prepared=True)
        sql_insert_query = """INSERT INTO Course (CourseID, CourseTitle, Credits, Department,
         Topic1, Topic2,Topic3, Topic4, Topic5, Topic6, Topic7, Topic8,Topic9, Topic10,
         Topic11, Topic12,Topic13,Topic14, Topic15, Topic16,Topic17, Topic18, Topic19, Topic20)
         VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"""

        insert_tuple = preparing_to_connect_to_database.insert_list_to_sql_tuple(insert_list)

        my_cursor.execute(sql_insert_query, insert_tuple)
        my_db.commit()
        my_cursor.close()
        my_db.close()
        return insert_list[0] + " has been successfully added to the database of courses!"
    except mysql.connector.Error as error:
        return "parameterized query failed {}".format(error)


def modify_course_row(insert_list):
    try:
        my_db = connection_to_mysql()
        my_cursor = my_db.cursor(prepared=True)
        sql_insert_query = """UPDATE Course SET CourseTitle = %s, Credits = %s, Department = %s,
         Topic1 = %s, Topic2 = %s,Topic3 = %s, Topic4 = %s, Topic5 = %s, Topic6 = %s, Topic7 = %s, Topic8 = %s,Topic9 = %s, Topic10 = %s,
         Topic11 = %s, Topic12 = %s,Topic13 = %s,Topic14 = %s, Topic15 = %s, Topic16 = %s,Topic17 = %s, Topic18 = %s, Topic19 = %s, Topic20 = %s
         WHERE CourseID = %s"""
        course_id = insert_list[0]
        insert_list.append(insert_list[0])
        insert_list.pop(0)

        insert_tuple = preparing_to_connect_to_database.insert_list_to_sql_tuple(insert_list)

        my_cursor.execute(sql_insert_query, insert_tuple)
        my_db.commit()
        my_cursor.close()
        my_db.close()
        return course_id + " has been successfully been modified in the database!"
    except mysql.connector.Error as error:
        return "parameterized query failed {}".format(error)


def get_course_row(the_course):
    course_info = ()
    try:
        my_db = connection_to_mysql()
        my_cursor = my_db.cursor(prepared=True)
        sql_insert_query = """SELECT * FROM Course WHERE CourseID = %s"""
        my_cursor.execute(sql_insert_query, tuple([the_course]))
        for course in my_cursor:
            course_info = list(course)
            break

        my_cursor.close()
        my_db.close()
        course_info.insert(0, "None")
        return course_info
    except mysql.connector.Error as error:
        return ["parameterized query failed {}".format(error)]


def insert_student_request_row(insert_list, request, request_key, home_path):
    try:
        my_db = connection_to_mysql()
        my_cursor = my_db.cursor(prepared=True)
        sql_insert_query = """INSERT INTO StudentRequest (RequestID,
        FirstNameCode, LastNameCode, UFIDCode, emailCode, 
        UFCourseID,
        FirstCourseID, FirstCourseTitle, FirstCredits, FirstUniversity, FirstDepartment, 
        FirstTerm, FirstGrade, FirstInstructorEmail, FirstTextbook, FirstAuthor, 
        IsSecondClass,
        SecondCourseID, SecondCourseTitle, SecondCredits, SecondUniversity, SecondDepartment, SecondTerm, SecondGrade, 
        SecondInstructorEmail, SecondTextbook, SecondAuthor,
        TopicLoc1, TopicLoc2,TopicLoc3, TopicLoc4, TopicLoc5, TopicLoc6, TopicLoc7, TopicLoc8,TopicLoc9, TopicLoc10,
        TopicLoc11, TopicLoc12,TopicLoc13,TopicLoc14, TopicLoc15, TopicLoc16,TopicLoc17, TopicLoc18, TopicLoc19, TopicLoc20,
        AmountFirstFiles, AmountSecondFiles, OtherComments)
        VALUES (%s,
        %s,%s,%s,%s,
        %s,
        %s,%s,%s,%s,%s,
        %s,%s,%s,%s,%s,
        %s,
        %s,%s,%s,%s,%s,%s,%s,
        %s,%s,%s,
        %s,%s,%s,%s,%s,%s,%s,%s,%s,%s,
        %s,%s,%s,%s,%s,%s,%s,%s,%s,%s,
        %s,%s,%s)
         """
        sql_key_insert_query = """INSERT INTO RequestKey (RequestKeyID, TheKey)
        VALUES (%s,%s)
        """

        insert_tuple = preparing_to_connect_to_database.insert_list_to_sql_tuple(insert_list)
        insert_key_tuple = tuple([insert_list[0], request_key])

        my_cursor.execute(sql_insert_query, insert_tuple)
        my_cursor.execute(sql_key_insert_query, insert_key_tuple)

        my_db.commit()
        my_cursor.close()
        my_db.close()

        getting_request_data_and_cleaning_it.put_files_into_directory(request, insert_list[0], home_path)
        return "Your Course Request has been successfully submitted, please look forward to a confirmation email sent to you!"
    except mysql.connector.Error as error:
        print("parameterized query failed {}".format(error))
        return "Error when sending query to database, please look over your information and try again."


def get_list_all_requests_by_single_course(the_course):
    """

    :param the_course: A string of a single courseID
    :return: A 2D list of all request in that course with 5 values RequestID, UFCourseID, TheDate, FirstName, LastName
    """
    try:
        my_db = connection_to_mysql()
        my_cursor = my_db.cursor(prepared=True)
        sql_insert_query = """SELECT StudentRequest.RequestID, UFCourseID, TheDate, FirstNameCode, LastNameCode, TheKey 
                              FROM StudentRequest 
                              JOIN RequestKey ON StudentRequest.RequestID = RequestKey.RequestKeyID
                              WHERE UFCourseID = %s
                              ORDER BY TheDate DESC"""
        my_cursor.execute(sql_insert_query, tuple([the_course]))
        requests_2D = []
        for request in my_cursor:
            cur_request_info = list(request)
            cur_key = request[5]
            cur_request_info[2] = cur_request_info[2].strftime("%b-%d-%Y")
            cur_request_info[3] = getting_request_data_and_cleaning_it.decode_data(cur_request_info[3], cur_key)
            cur_request_info[4] = getting_request_data_and_cleaning_it.decode_data(cur_request_info[4], cur_key)
            requests_2D.append(cur_request_info[:5])
        my_cursor.close()
        my_db.close()
        return requests_2D
    except mysql.connector.Error as error:
        return ["parameterized query failed {}".format(error)]


def check_if_already_in_all_requests_by_single_course(the_course, session_ufid):
    """

    :param the_course: A string of a single courseID and a string of the user's UFID
    :return: a list of two booleans [True, False]
    First one states whether the query happened successfully
    Second one states whether the udif is in it
    """
    try:
        exists_request = False
        my_db = connection_to_mysql()
        my_cursor = my_db.cursor(prepared=True)
        sql_insert_query = """SELECT StudentRequest.RequestID, UFIDCode, UFCourseID, TheKey 
                              FROM StudentRequest 
                              JOIN RequestKey ON StudentRequest.RequestID = RequestKey.RequestKeyID
                              WHERE UFCourseID = %s"""
        my_cursor.execute(sql_insert_query, tuple([the_course]))
        for request in my_cursor:
            cur_request_info = list(request)
            cur_key = request[3]
            cur_request_info[1] = getting_request_data_and_cleaning_it.decode_data(cur_request_info[1], cur_key)
            if session_ufid == cur_request_info[1]:
                exists_request = True
        my_cursor.close()
        my_db.close()
        return [True, exists_request]
    except mysql.connector.Error as error:
        print("parameterized query failed {}".format(error))
        return [False, False]


def check_if_already_in_all_archive_by_single_course(the_course, session_ufid):
    """

    :param the_course: A string of a single courseID and a string of the user's UFID
    :return: a list of two booleans [True, False]
    First one states whether the query happened successfully
    Second one states whether the udif is in it
    """
    try:
        exists_request = False
        my_db = connection_to_mysql()
        my_cursor = my_db.cursor(prepared=True)
        sql_insert_query = """SELECT ID, HashedUFID, UFCourseID
                              FROM ApprovedRequest 
                              WHERE UFCourseID = %s"""
        my_cursor.execute(sql_insert_query, tuple([the_course]))
        for request in my_cursor:
            print(request)
            cur_request_info = list(request)

            if getting_request_data_and_cleaning_it.check_password(session_ufid, cur_request_info[1]):
                exists_request = True
        my_cursor.close()
        my_db.close()
        return [True, exists_request]
    except mysql.connector.Error as error:
        print("parameterized query failed {}".format(error))
        return [False, False]


def amount_request_in_a_course(the_course):
    """

    :param the_course: A string of a single courseID and a string of the user's UFID
    :return: a list of two booleans [True, False]
    First one states whether the query happened successfully
    Second one states whether the udif is in it
    """
    try:
        exists_request = False
        my_db = connection_to_mysql()
        my_cursor = my_db.cursor(prepared=True)
        sql_insert_query = """SELECT count(*) FROM studentrequest 
                              WHERE UFCourseID = %s;"""
        my_cursor.execute(sql_insert_query, tuple([the_course]))
        for request in my_cursor:
            cur_request_info = list(request)
        my_cursor.close()
        my_db.close()
        return [True, cur_request_info[0]]
    except mysql.connector.Error as error:
        print("parameterized query failed {}".format(error))
        return [False, "parameterized query failed {}".format(error)]


def get_request_and_course_row(request_id):
    request_info = []
    try:
        my_db = connection_to_mysql()
        my_cursor = my_db.cursor(prepared=True)
        sql_insert_query = """SELECT RequestKey.thekey, StudentRequest.*, Course.*  FROM StudentRequest
                              JOIN RequestKey ON StudentRequest.RequestID = RequestKey.RequestKeyID
                              JOIN Course ON StudentRequest.UFCourseID = Course.CourseID
                              WHERE RequestID = %s"""

        my_cursor.execute(sql_insert_query, tuple([request_id]))
        for request_id in my_cursor:
            request_info = list(request_id)
            break

        my_cursor.close()
        my_db.close()
        request_info.insert(0, "None")
        return request_info
    except mysql.connector.Error as error:
        return "parameterized query failed {}".format(error)


def remove_a_course(the_course):
    """

    :param the_course: A string of a single courseID and a string of the user's UFID
    :return: a list of two booleans [True, False]
    First one states whether the query happened successfully
    Second one states whether the udif is in it
    """
    try:
        my_db = connection_to_mysql()
        my_cursor = my_db.cursor(prepared=True)
        sql_insert_query = """Delete FROM Course
                              WHERE CourseID = %s"""
        my_cursor.execute(sql_insert_query, tuple([the_course]))
        my_db.commit()
        my_cursor.close()
        my_db.close()
        return "Course " + the_course + " has been successfully removed from the course database"
    except mysql.connector.Error as error:
        return "parameterized query failed {}".format(error)


def remove_row_from_student_request(request_id, uf_course_id, home_path):
    try:
        my_db = connection_to_mysql()
        my_cursor = my_db.cursor(prepared=True)
        sql_insert_query = """Delete FROM StudentRequest
                              WHERE RequestID = %s"""
        sql_key_insert_query = """Delete FROM RequestKey
                              WHERE RequestKeyID = %s"""

        my_cursor.execute(sql_insert_query, tuple([request_id]))
        my_cursor.execute(sql_key_insert_query, tuple([request_id]))
        my_db.commit()
        my_cursor.close()
        my_db.close()
        getting_request_data_and_cleaning_it.remove_files_and_directory(request_id, uf_course_id, home_path)
        return "Student request has been successfully deleted from the database and file directory!"
    except mysql.connector.Error as error:
        return "parameterized query failed {}".format(error)


def insert_student_request_archive(insert_list):
    try:
        my_db = connection_to_mysql()
        my_cursor = my_db.cursor(prepared=True)
        sql_insert_query = """INSERT INTO ApprovedRequest (ID,
        FirstNameCode, LastNameCode, HashedUFID, emailCode,
        UFCourseID, UFCourseTitle, UFCredits, UFDepartment,
        FirstCourseID, FirstCourseTitle, FirstCredits, FirstUniversity, FirstTerm, FirstGrade,
        IsSecondClass,
        SecondCourseID, SecondCourseTitle, SecondCredits, SecondUniversity, SecondTerm, SecondGrade,
        FacultyComments)
        VALUES (%s,
        %s,%s,%s,%s,
        %s,%s,%s,%s,
        %s,%s,%s,%s,%s,%s,
        %s,
        %s,%s,%s,%s,%s,%s,
        %s)
         """
        sql_key_insert_query = """INSERT INTO ApprovedKey (KeyID, TheKey)
                VALUES (%s,%s)
                 """
        insert_tuple = preparing_to_connect_to_database.insert_list_to_sql_tuple(insert_list)
        my_cursor.execute(sql_insert_query, insert_tuple)
        my_db.commit()
        my_cursor.close()
        my_db.close()
        return "Student has been successfully added to the archive."
    except mysql.connector.Error as error:
        return "parameterized query failed {}".format(error)


def insert_session(insert_list):
    try:
        my_db = connection_to_mysql()
        my_cursor = my_db.cursor(prepared=True)
        sql_insert_query = """INSERT INTO Session (SessionID, FirstNameCode, LastNameCode, UFIDCode,
         emailCode, AuthCode)
         VALUES (%s,%s,%s,%s,%s,%s)"""

        insert_tuple = preparing_to_connect_to_database.insert_list_to_sql_tuple(insert_list)

        my_cursor.execute(sql_insert_query, insert_tuple)
        my_db.commit()
        my_cursor.close()
        my_db.close()
        return insert_list[0] + " has been successfully added to the database of courses!"
    except mysql.connector.Error as error:
        return "parameterized query failed {}".format(error)


def get_session_authorization(session_id):
    authorization_info = []
    try:
        my_db = connection_to_mysql()
        my_cursor = my_db.cursor(prepared=True)
        sql_insert_query = """SELECT AuthCode FROM Session WHERE SessionID = %s"""
        my_cursor.execute(sql_insert_query, tuple([session_id]))
        for auth in my_cursor:
            authorization_info = list(auth)
            break
        my_cursor.close()
        my_db.close()
        return authorization_info[0]
    except mysql.connector.Error as error:
        return "parameterized query failed {}".format(error)


def get_session_ufid(session_id):
    ufid_info = []
    try:
        my_db = connection_to_mysql()
        my_cursor = my_db.cursor(prepared=True)
        sql_insert_query = """SELECT UFIDCODE FROM Session WHERE SessionID = %s"""
        my_cursor.execute(sql_insert_query, tuple([session_id]))
        for ufid in my_cursor:
            ufid_info = list(ufid)
            break
        my_cursor.close()
        my_db.close()
        return ufid_info[0]
    except mysql.connector.Error as error:
        return "parameterized query failed {}".format(error)


def get_session_name_ufid(session_id):
    session_user_info = []
    try:
        my_db = connection_to_mysql()
        my_cursor = my_db.cursor(prepared=True)
        sql_insert_query = """SELECT FirstNameCode, LastNameCode, UFIDCode FROM Session WHERE SessionID = %s"""
        my_cursor.execute(sql_insert_query, tuple([session_id]))
        for info in my_cursor:
            session_user_info = list(info)
            break
        my_cursor.close()
        my_db.close()
        return session_user_info
    except mysql.connector.Error as error:
        return "parameterized query failed {}".format(error)


if __name__ == '__main__':
    red = amount_request_in_a_course('WAT5999')
    print(red)
