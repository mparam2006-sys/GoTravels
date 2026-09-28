from database import get_db_connection


def add_passengers(booking_id, passengers):
    connection = get_db_connection()

    try:
        cursor = connection.cursor(dictionary=True)

        # Check whether booking exists
        cursor.execute(
            """
            SELECT booking_id
            FROM bookings
            WHERE booking_id = %s
            """,
            (booking_id,)
        )

        booking = cursor.fetchone()

        if not booking:
            return {
                "success": False,
                "message": "Booking not found"
            }

        # Insert passenger details
        query = """
            INSERT INTO passengers
            (
                booking_id,
                full_name,
                age,
                gender,
                id_type,
                id_number
            )
            VALUES (%s, %s, %s, %s, %s, %s)
        """

        for passenger in passengers:
            cursor.execute(
                query,
                (
                    booking_id,
                    passenger["full_name"],
                    passenger["age"],
                    passenger["gender"],
                    passenger.get("id_type"),
                    passenger.get("id_number")
                )
            )

        connection.commit()

        cursor.close()

        return {
            "success": True,
            "message": "Passenger details added successfully",
            "booking_id": booking_id,
            "passenger_count": len(passengers)
        }

    except Exception as e:
        connection.rollback()

        return {
            "success": False,
            "message": str(e)
        }

    finally:
        connection.close()