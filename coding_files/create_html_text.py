from coding_files import connection_to_database


def html_list_of_courses():
    """
    Creates a list of courseID's and CourseTitles to then be wrapped in a HTML select tag
    :return: string of course options to be wrapped in html select tag
    """
    course_ids, courses = connection_to_database.get_list_all_sorted_course_ids_and_courses()
    html_str = ""
    for i in range(len(courses)):
        html_str += '<option value="' + str(course_ids[i]) + '">' + str(courses[i]) + '</option>'
    return html_str


def html_add_course_attributes():
    attributes = ["Machine code, source code, compilation, & execution",
                  "Variables, data types, arithmetic, & basic IO", "Selection and Flow Control (if/else; for; while)",
                  "Methods / functions (creation, invocation)",
                  "Objects, classes, and inheritance (including abstract classes and interfaces)",
                  "Source control systems (like Git or SVN)",
                  "Use of a debugger suite", "Try / catch / exception handling",
                  "Octal / hex / binary numbers", "Big-O notation and basic complexity analysis",
                  "Logic fundamentals (including contrapositive /exclusive or / truth tables)",
                  "Programming paradigms (imperative, procedural, object-oriented, functional)",
                  "Recursion theory & coding",
                  "Stack and heap, and how they relate to variablereferences, objects, and value types", " ",
                  " ", " ", " ", " ", " "]
    html_str = ""
    for i in range(20):
        html_str += '<div class="item">'
        html_str += '<label for="attribute' + str(i + 1) + '">Attribute ' + str(i + 1)
        if i == 0:
            html_str += '<span>*</span>'
        html_str +='</label>'
        html_str += '<input type="text" name="attribute' + str(i + 1) + '" placeholder="' + attributes[i] + '" maxlength="150"'
        if i == 0:
            html_str += 'required'
        html_str += '/>'

        html_str += '</div>'
    return html_str


def html_modify_course_attributes(attributes):
    for i in range(len(attributes)):
        if attributes[i] == "N/A":
            attributes[i] = ""

    html_str = ""
    for i in range(20):
        html_str += '<div class="item">'
        html_str += '<label for="attribute' + str(i + 1) + '">Attribute ' + str(i + 1)
        if i == 0:
            html_str += '<span>*</span>'
        html_str += ": " + attributes[i]
        html_str +='</label>'
        html_str += '<input type="text" name="attribute' + str(i + 1) + '" value="' + attributes[i] + '" maxlength="150"'
        if i == 0:
            html_str += 'required'
        html_str += '/>'

        html_str += '</div>'
    return html_str


def html_checkbox_attributes(attributes):
    html_str = ""
    html_str += '<div style="display: flex;flex-wrap: nowrap; flex-direction: column; justify-content: space-between">'
    for i in range(20):
        if attributes[i] == "" or attributes[i] == "N/A":
            continue
        html_str += '<div style="display: flex;flex-wrap: nowrap; flex-direction: row;  margin-bottom: 5px; justify-content: flex-start">'
        html_str += '<div style="">'
        html_str += '<input type="checkbox" class="checkbox" id="attribute' + str(i+1) + '" value="Yes' + str(i+1) + '" >'
        html_str += '</div>'
        html_str += '<div style="">'
        html_str += '<span style="font-size: 16px; display: inline;">  ' + attributes[i] + '</span><br>'
        html_str += '</div></div>'
    html_str += '</div>'
    return html_str


if __name__ == '__main__':
    print(html_add_course_attributes())
