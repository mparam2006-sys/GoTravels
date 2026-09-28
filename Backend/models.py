import bcrypt
from database import get_db_connection


def create_user(full_name, email, phone, password):
    connection = get_db_connection()
    cursor = connection.cursor()

    password_hash = bcrypt.hashpw(
        password.encode("utf-8"),
        bcrypt.gensalt()
    ).decode("utf-8")

    query = """
        INSERT INTO users
        (full_name, email, phone, password_hash)
        VALUES (%s, %s, %s, %s)
    """

    values = (full_name, email, phone, password_hash)

    cursor.execute(query, values)
    connection.commit()

    user_id = cursor.lastrowid

    cursor.close()
    connection.close()

    return user_id


def login_user(email, password):
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)

    query = """
        SELECT user_id, full_name, email, phone, role, status, password_hash
        FROM users
        WHERE email = %s
    """

    cursor.execute(query, (email,))
    user = cursor.fetchone()

    cursor.close()
    connection.close()

    if not user:
        return None

    if not bcrypt.checkpw(
        password.encode("utf-8"),
        user["password_hash"].encode("utf-8")
    ):
        return None

    user.pop("password_hash")

    return user


def get_all_travel_services():
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)

    query = """
        SELECT
            ts.service_id,
            ts.service_name,
            ts.service_number,
            st.type_name AS service_type,
            p.provider_name,
            ts.description,
            ts.status
        FROM travel_services ts
        JOIN service_types st
            ON ts.service_type_id = st.service_type_id
        JOIN providers p
            ON ts.provider_id = p.provider_id
    """

    cursor.execute(query)
    services = cursor.fetchall()

    cursor.close()
    connection.close()

    return services


def search_travel_services(from_city, to_city, travel_date, service_type=None):
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)

    query = """
        SELECT
            s.schedule_id,
            ts.service_id,
            st.type_name AS service_type,
            p.provider_name,
            ts.service_name,
            ts.service_number,
            dl.location_name AS departure_location,
            dl.city AS departure_city,
            al.location_name AS arrival_location,
            al.city AS arrival_city,
            s.departure_datetime,
            s.arrival_datetime,
            s.price,
            s.total_capacity,
            s.available_capacity,
            s.status
        FROM schedules s
        JOIN travel_services ts
            ON s.service_id = ts.service_id
        JOIN service_types st
            ON ts.service_type_id = st.service_type_id
        JOIN providers p
            ON ts.provider_id = p.provider_id
        JOIN locations dl
            ON s.departure_location_id = dl.location_id
        JOIN locations al
            ON s.arrival_location_id = al.location_id
        WHERE dl.city = %s
          AND al.city = %s
          AND DATE(s.departure_datetime) = %s
          AND s.status = 'AVAILABLE'
          AND s.available_capacity > 0
    """

    values = [from_city, to_city, travel_date]

    if service_type:
        query += " AND st.type_name = %s"
        values.append(service_type.upper())

    query += " ORDER BY s.departure_datetime"

    cursor.execute(query, values)
    results = cursor.fetchall()

    cursor.close()
    connection.close()

    return results