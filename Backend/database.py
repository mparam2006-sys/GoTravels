import mysql.connector


def get_db_connection():
    connection = mysql.connector.connect(
        host="localhost",
        user="root",
        password="Naveen@02",
        database="gotravels"
    )

    return connection