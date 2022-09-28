import mysql.connector
from mysql.connector import errorcode
from coding_files import declutter_main_page
import os


def connection_to_mysql(is_online = False):
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
    my_db = connection_to_mysql()
    my_cursor = my_db.cursor(prepared=True)
    my_cursor.execute("""SELECT CourseID FROM Course""")

    course_id_array = []
    for course in my_cursor:
        course_id_array.append(course[0])
    my_cursor.close()
    my_db.close()
    return course_id_array


def get_list_all_sorted_course_ids_and_courses():
    """

    :return: A tuple of a sorted list of course_ids then a sorted list of 'corse_ids: course_titles'
    """
    my_db = connection_to_mysql()
    my_cursor = my_db.cursor(prepared=True)
    my_cursor.execute("""SELECT CourseID, CourseTitle FROM Course""")
    courses = []
    course_ids = []
    for course in my_cursor:
        courses.append(course[0] + ": " + course[1])
        course_ids.append(course[0])
    my_cursor.close()
    my_db.close()
    course_ids.sort()
    courses.sort()
    return (course_ids, courses)


def insert_course_row(insert_list):
    try:
        my_db = connection_to_mysql()
        my_cursor = my_db.cursor(prepared=True)
        sql_insert_query = """INSERT INTO Course (CourseID, CourseTitle, Credits, Department,
         Topic1, Topic2,Topic3, Topic4, Topic5, Topic6, Topic7, Topic8,Topic9, Topic10,
         Topic11, Topic12,Topic13,Topic14, Topic15, Topic16,Topic17, Topic18, Topic19, Topic20)
         VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"""

        insert_tuple = declutter_main_page.insert_list_to_sql_tuple(insert_list)

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

        insert_tuple = declutter_main_page.insert_list_to_sql_tuple(insert_list)

        my_cursor.execute(sql_insert_query, insert_tuple)
        my_db.commit()
        my_cursor.close()
        my_db.close()
        return course_id + " has been successfully been modified in the database!"
    except mysql.connector.Error as error:
        return "parameterized query failed {}".format(error)


def get_course_row(the_couse):
    course_dict = {
        "error": "None", "course_id": "", "course_title":""
    }

    course_info = ()
    try:
        my_db = connection_to_mysql()
        my_cursor = my_db.cursor(prepared=True)
        sql_insert_query = """SELECT * FROM Course WHERE CourseID = %s"""
        my_cursor.execute(sql_insert_query, tuple([the_couse]))
        for course in my_cursor:
            course_info = list(course)
            break

        my_cursor.close()
        my_db.close()
        course_info.insert(0, "None")
        return course_info
    except mysql.connector.Error as error:
        return ["parameterized query failed {}".format(error)]

if __name__ == '__main__':
    print(get_course_row("CAP3020"))
