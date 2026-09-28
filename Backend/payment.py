import uuid
from database import get_db_connection


def process_payment(booking_id, payment_method):
    connection = get_db_connection()

    try:
        cursor = connection.cursor(dictionary=True)

        # Get booking details
        query = """
            SELECT
                booking_id,
                total_amount,
                booking_status
            FROM bookings
            WHERE booking_id = %s
        """

        cursor.execute(query, (booking_id,))
        booking = cursor.fetchone()

        if not booking:
            return {
                "success": False,
                "message": "Booking not found"
            }

        if booking["booking_status"] == "CANCELLED":
            return {
                "success": False,
                "message": "Cannot make payment for a cancelled booking"
            }

        # Check if payment already exists
        cursor.execute(
            """
            SELECT payment_id
            FROM payments
            WHERE booking_id = %s
              AND payment_status = 'SUCCESS'
            """,
            (booking_id,)
        )

        existing_payment = cursor.fetchone()

        if existing_payment:
            return {
                "success": False,
                "message": "Payment has already been completed"
            }

        # Generate transaction ID
        transaction_id = "TXN" + uuid.uuid4().hex[:10].upper()

        # Insert payment
        insert_query = """
            INSERT INTO payments
            (
                booking_id,
                transaction_id,
                amount,
                payment_method,
                payment_status
            )
            VALUES (%s, %s, %s, %s, 'SUCCESS')
        """

        cursor.execute(
            insert_query,
            (
                booking_id,
                transaction_id,
                booking["total_amount"],
                payment_method.upper()
            )
        )

        # Update booking status
        update_query = """
            UPDATE bookings
            SET booking_status = 'CONFIRMED'
            WHERE booking_id = %s
        """

        cursor.execute(update_query, (booking_id,))

        connection.commit()

        payment_id = cursor.lastrowid

        cursor.close()

        return {
            "success": True,
            "message": "Payment successful",
            "payment_id": payment_id,
            "booking_id": booking_id,
            "transaction_id": transaction_id,
            "amount": float(booking["total_amount"]),
            "payment_method": payment_method.upper(),
            "payment_status": "SUCCESS"
        }

    except Exception as e:
        connection.rollback()

        return {
            "success": False,
            "message": str(e)
        }

    finally:
        connection.close()