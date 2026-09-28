from database import get_db_connection


def get_user_bookings(user_id):
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)

    query = """
        SELECT
            b.booking_id,
            b.booking_reference,
            b.booking_date,
            b.total_amount,
            b.booking_status,

            ts.service_name,
            ts.service_number,
            st.type_name AS service_type,
            p.provider_name,

            dl.city AS departure_city,
            al.city AS arrival_city,

            s.departure_datetime,
            s.arrival_datetime,

            COALESCE(
                SUM(CASE
                    WHEN pay.payment_status = 'SUCCESS' THEN 1
                    ELSE 0
                END),
                0
            ) AS payment_completed

        FROM bookings b

        JOIN schedules s
            ON b.schedule_id = s.schedule_id

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

        LEFT JOIN payments pay
            ON b.booking_id = pay.booking_id

        WHERE b.user_id = %s

        GROUP BY
            b.booking_id,
            b.booking_reference,
            b.booking_date,
            b.total_amount,
            b.booking_status,
            ts.service_name,
            ts.service_number,
            st.type_name,
            p.provider_name,
            dl.city,
            al.city,
            s.departure_datetime,
            s.arrival_datetime

        ORDER BY b.booking_date DESC
    """

    cursor.execute(query, (user_id,))
    bookings = cursor.fetchall()

    cursor.close()
    connection.close()

    for booking in bookings:
        booking["payment_completed"] = bool(
            booking["payment_completed"]
        )

    return bookings