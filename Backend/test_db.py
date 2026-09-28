from database import get_db_connection

try:
    connection = get_db_connection()

    if connection.is_connected():
        print("Database connection successful!")

    connection.close()

except Exception as e:
    print("Database connection failed:", e)