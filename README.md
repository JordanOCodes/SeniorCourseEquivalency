# SeniorCourseEquivalency
Senior Project

This project is public while faculty look it over, it will return private soon.

This is the senior project for the course equivalency. It is a webapplication for course equivalency requests.
It is written in the programming languages python, html, css, javascript. Using the web framework Flask.

## How to install

This application is meant to run on a specific website, however, if you wish to run it on a local machine you must know a few things
1. In coding_files.connection_to_database.py connection_to_mysql(is_online=True), change this variable to false, and set it to your own local host resister.
If you wish to run it online as it's intended, there should be a file outside of the directory that that function calls
2) In coding_files.sending_emails.py send_email(to_email, message): the current email and passcode is an old email and passcode of the original creator, it won't be working for long, feel free to change this for proper email sending.
3) mysql_add.txt is a bunch of SQL queries to be able to create your own mysql set up to run a database along with this application.

In the proper online use a file index.cgi calls this function in order to work properly.
A .htaccess file in htdocs calls this cgi file when the index page is called.

## How to use
