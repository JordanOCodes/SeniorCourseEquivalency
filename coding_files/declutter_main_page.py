def class_args_to_list(form):
    course_info_list = [form["course_id"], form["course_title"], form["credits"], form["department"]]
    attributes_list = [form["attribute1"],
                       form["attribute2"],
                       form["attribute3"], form["attribute4"], form["attribute5"], form["attribute6"],
                       form["attribute7"],
                       form["attribute8"], form["attribute9"], form["attribute10"], form["attribute11"],
                       form["attribute12"],
                       form["attribute13"], form["attribute14"], form["attribute15"], form["attribute16"],
                       form["attribute17"],
                       form["attribute18"], form["attribute19"], form["attribute20"]]

    temp_list = []
    for i in range(len(attributes_list)):  # Create a list of attributes, not including empty ""
        if attributes_list[i] != "":
            temp_list.append(attributes_list[i])
    for i in range(len(attributes_list) - len(temp_list)):  # append "" to temp until you have 20 attributes
        temp_list.append("")
    for i in range(len(temp_list)):  # append the attributes to the course info list
        course_info_list.append(temp_list[i])

    return course_info_list


def insert_list_to_sql_tuple(insert_list):
    for i in range(len(insert_list)):
        if insert_list[i] == '':
            insert_list[i] = 'N/A'
    return tuple(insert_list)

if __name__ == '__main__':
    print("hello")
