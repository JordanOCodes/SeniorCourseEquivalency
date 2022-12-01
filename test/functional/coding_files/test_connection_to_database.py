from coding_files import connection_to_database


def test_connection_to_mysql(mysql_connection):
    assert mysql_connection is not None and mysql_connection.is_connected()



