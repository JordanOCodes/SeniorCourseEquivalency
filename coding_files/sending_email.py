# Import smtplib for the actual sending function
import smtplib


def send_email(to_email, message):
    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as connection:
        email_address = 'jordano.life@gmail.com'
        email_password = 'sqnicvllpulqkgaa'
        connection.login(email_address, email_password)
        connection.sendmail(from_addr=email_address, to_addrs=to_email,
                            msg=message)


def student_request_confirmation(to_email, first_name, last_name, course_id, course_title):
    """
    to_email, first_name, last_name, course_id, course_title
    :return: A String that will easily format into an email
    """
    message = f"""subject:CISE Course Equivalency Request Confirmation \n\n
    \nDear {first_name} {last_name},
    \nThank you for submitting a CISE Course Equivalence Form for {course_id}: {course_title}
    \nThis email is confirmation that your request is being sent for further processing.
    \nPlease await for the proper faculty members to review your request.
    \n
    \nThank you,
    \nCISE Department
    """
    send_email(to_email, message)


def student_request_denial(to_email, first_name, last_name, course_id, course_title, faculty_comments):
    """
    to_email, first_name, last_name, course_id, course_title
    :return: A String that will easily format into an email
    """
    message = f"""subject:CISE Course Equivalency Request Denial\n\n
    \nDear {first_name} {last_name},
    \nWe are sorry to inform you that your CISE Course Equivalence Form for {course_id}: {course_title} has been denied.
    \nThis email is confirmation that request has been denied.
    \nHere are the comments that has been given about your Request from a Faculty Member:
    \n
    \n"{faculty_comments}"
    \n
    \nThank you,
    \nCISE Department
    """
    send_email(to_email, message)


def student_request_approve(to_email, first_name, last_name, course_id, course_title, faculty_comments):
    """
    to_email, first_name, last_name, course_id, course_title
    :return: A String that will easily format into an email
    """
    message = f"""subject:CISE Course Equivalency Request Approval!!!\n\n
    \nDear {first_name} {last_name},
    \nWe are happy to inform you that your CISE Course Equivalence Form for {course_id}: {course_title} has been approved!!
    \nThis email is confirmation that your request has been approve!!!
    \nHere are the comments that has been given about your Request from a Faculty Member:
    \n
    \n"{faculty_comments}"
    \n
    \nThank you,
    \nCISE Department
    """
    send_email(to_email, message)


def faculty_email_reminder(to_email, course_id_list, course_title_list, faculty_comments):
    """
    to_email, first_name, last_name, course_id, course_title
    :return: A String that will easily format into an email
    """
    message = f"""subject:CISE Course Equivalency Request Await You!\n\n
    \nDear Appropriate Faculty Member,
    \nThere are course requests awaiting you for the following classes:"""
    length = len(course_id_list)
    if length > 3:
        length = 3
    for i in range(length):
        message += f"\n{course_id_list[i]}: {course_title_list[i]}."
    if len(course_id_list > 3):
        message += "\nAnd more!"
    message += """\nPlease view them at your convince.
    \nThank you,
    \nCISE Department
    """
    send_email(to_email, message)


if __name__ == '__main__':
    student_request_confirmation("SkippySenior@yahoo.com", "Jordan", "Oldham", "COP3400", "Programming Fundamentals 32")
    student_request_approve("SkippySenior@yahoo.com", "Jordan", "Oldham", "COP3400", "Programming Fundamentals 32",
                            "Thank you for applying the appropriate files, have a nice time at UF!")
    student_request_denial("SkippySenior@yahoo.com", "Jordan", "Oldham", "COP3400", "Programming Fundamentals 32",
                            "Thank you for applying the appropriate files, have a nice time at UF!")