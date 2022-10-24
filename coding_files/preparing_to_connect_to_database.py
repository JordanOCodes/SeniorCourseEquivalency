from coding_files import connection_to_database
import bcrypt
import os
from werkzeug.utils import secure_filename

ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg'}


def insert_list_to_sql_tuple(insert_list):
    for i in range(len(insert_list)):
        if insert_list[i] == '':
            insert_list[i] = 'N/A'
    return tuple(insert_list)


def get_all_request_for_all_allowed_courses(list_of_allowed_courses):
    list_of_requests = []
    for i in range(len(list_of_allowed_courses)):
        list_of_request_for_single_course = connection_to_database.get_list_all_requests_by_single_course(list_of_allowed_courses[i])
        for j in range(len(list_of_request_for_single_course)):
            list_of_requests.append(list_of_request_for_single_course[j])

    return list_of_requests


if __name__ == '__main__':
    print("yellowstone")