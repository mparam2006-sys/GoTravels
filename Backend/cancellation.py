from database import get_db_connection


def cancel_booking(booking_id, reason):
    connection = get_db_connection()

    try:
        connection.start_transaction()

        cursor = connection.cursor(dictionary=True)

        # Get booking details
        booking_query = """
            SELECT
                b.booking_id,
                b.schedule_id,
                b.total_amount,
                b.booking_status,
                s.available_capacity
            FROM bookings b
            JOIN schedules s
                ON b.schedule_id = s.schedule_id
            WHERE b.booking_id = %s
            FOR UPDATE
        """

        cursor.execute(booking_query, (booking_id,))
        booking = cursor.fetchone()

        if not booking:
            connection.rollback()
            return {
                "success": False,
                "message": "Booking not found"
            }

        if booking["booking_status"] == "CANCELLED":
            connection.rollback()
            return {
                "success": False,
                "message": "Booking is already cancelled"
            }

        # Count passengers for this booking
        cursor.execute(
            """
            SELECT COUNT(*) AS passenger_count
            FROM passengers
            WHERE booking_id = %s
            """,
            (booking_id,)
        )

        passenger_data = cursor.fetchone()
        passenger_count = passenger_data["passenger_count"]

        # If no passenger records exist, use 1 as fallback
        if passenger_count < 1:
            passenger_count = 1

        # Update booking status
        cursor.execute(
            """
            UPDATE bookings
            SET booking_status = 'CANCELLED'
            WHERE booking_id = %s
            """,
            (booking_id,)
        )

        # Restore available capacity
        cursor.execute(
            """
            UPDATE schedules
            SET available_capacity = available_capacity + %s
            WHERE schedule_id = %s
            """,
            (passenger_count, booking["schedule_id"])
        )

        # Create cancellation record
        cursor.execute(
            """
            INSERT INTO cancellations
            (
                booking_id,
                reason,
                refund_amount,
                refund_status
            )
            VALUES (%s, %s, %s, 'PROCESSED')
            """,
            (
                booking_id,
                reason,
                booking["total_amount"]
            )
        )

        # Mark successful payment as refunded
        cursor.execute(
            """
            UPDATE payments
            SET payment_status = 'REFUNDED'
            WHERE booking_id = %s
              AND payment_status = 'SUCCESS'
            """,
            (booking_id,)
        )

        connection.commit()

        cursor.close()

        return {
            "success": True,
            "message": "Booking cancelled successfully",
            "booking_id": booking_id,
            "refund_amount": float(booking["total_amount"]),
            "refund_status": "PROCESSED",
            "booking_status": "CANCELLED"
        }

    except Exception as e:
        connection.rollback()

        return {
            "success": False,
            "message": str(e)
        }

    finally:
        connection.close()