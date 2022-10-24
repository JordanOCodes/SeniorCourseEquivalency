from coding_files import connection_to_database


def html_add_course_topics():
    topics = ["Machine code, source code, compilation, & execution",
              "Variables, data types, arithmetic, & basic IO", "Selection and Flow Control (if/else; for; while)",
              "Methods / functions (creation, invocation)",
              "Objects, classes, and inheritance (including abstract classes and interfaces)",
              "Source control systems (like Git or SVN)",
              "Use of a debugger suite", "Try / catch / exception handling",
              "Octal / hex / binary numbers", "Big-O notation and basic complexity analysis",
              "Logic fundamentals (including contrapositive /exclusive or / truth tables)",
              "Programming paradigms (imperative, procedural, object-oriented, functional)",
              "Recursion theory & coding",
              "Stack and heap, and how they relate to variable references, objects, and value types", " ",
              " ", " ", " ", " ", " "]
    html_str = ""
    for i in range(20):
        html_str += '<div class="item">'
        html_str += '<label for="topic' + str(i + 1) + '">Topic ' + str(i + 1)
        if i == 0:
            html_str += '<span>*</span>'
        html_str += '</label>'
        html_str += '<input type="text" name="topic' + str(i + 1) + '" placeholder="' + topics[i] + '" maxlength="150"'
        if i == 0:
            html_str += 'required'
        html_str += '/>'

        html_str += '</div>'
    return html_str


def html_topics(topics):
    html_str = ""
    html_str += '<ol>'
    for i in range(20):
        if topics[i] == "" or topics[i] == "N/A":
            continue
        html_str += '<li>  ' + topics[i] + '</li>'
    html_str += '</ol>'
    return html_str


def list_of_html_topics(topics):
    list_of_topics = []
    for i in range(20):
        html_str = '<p id="list_of_html_topics_' + str(i) + '" style="display:'
        if topics[i] == "" or topics[i] == "N/A":
            html_str += 'none" class="list_of_html_topics_hidden"'
        else:
            html_str += '" class="list_of_html_topics_display"'
        html_str += '> <b> ' + str(i + 1) + ". " + topics[i] + '</b></p>'
        html_str += '<div class="topic_student_request" id="container' + str(i) + '"></div>'
        list_of_topics.append(html_str)
    return list_of_topics


def list_of_html_topics_visibility(topics):
    list_of_topics_visibility = []
    for i in range(20):
        html_str = 'display: '
        if topics[i] == "" or topics[i] == "N/A":
            html_str += 'none'
        else:
            html_str += " "
        list_of_topics_visibility.append(html_str)

    return list_of_topics_visibility


def html_list_of_request_select(list_of_requests):
    """
    list of request = 2Darray each 5 values RequestID, UFCourseID, TheDate, FirstName, LastName
    Creates a list of requests to then be wrapped in a HTML select tag
    :return: string of course options to be wrapped in html select tag
    """

    html_str = ""
    for i in range(len(list_of_requests)):
        html_str += '<option value="' + str(list_of_requests[i][0]) + '">' + str(list_of_requests[i][1]) + ', ' + \
                    str(list_of_requests[i][2]) + ', ' + str(list_of_requests[i][3]) + ' ' + str(
            list_of_requests[i][4]) + '</option>'
    return html_str


def html_tabs(list_of_files, request_info_dict):
    amt_first_class_files = int(request_info_dict["AmountFirstFiles"])
    is_there_a_second_class = int(request_info_dict["IsSecondClass"])

    html_tabs = ""
    tab_index = 0
    for i in range(len(list_of_files)):
        tab_title_text = "<b>"
        if is_there_a_second_class == 1:
            if i < amt_first_class_files:
                tab_title_text += "First Class: "
            else:
                tab_title_text += "Second Class: "
        if i == 0 or amt_first_class_files - i == 0:
            tab_title_text += "Syllabus</b><br>"
        elif i == 1 or i - amt_first_class_files == 1:
            tab_title_text += "Catalog</b><br>"
        else:
            tab_title_text += "Extra</b><br>"
        tab_title_text += list_of_files[i]

        if tab_index == 0:
            html_tabs += '<div class="tab" style="display:flex; flex-direction: row; justify-content: flex-start;">'

        html_tabs += '<button type="button" id="tab' + str(i) + '" class="tablinks" '
        html_tabs += 'value="' + str(i) + '" '
        html_tabs += 'onclick="openFile(this.id, \'file' + str(i) + '\')" >'
        html_tabs += tab_title_text + '</button>'

        if tab_index == 3 or i == amt_first_class_files - 1 or i == len(list_of_files) - 1:
            html_tabs += '</div>'
            tab_index = 0
        else:
            tab_index += 1

    return html_tabs




if __name__ == '__main__':
    print(html_add_course_topics())
