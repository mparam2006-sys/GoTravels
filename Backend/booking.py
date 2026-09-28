import uuid
from database import get_db_connection


def create_booking(user_id, schedule_id, passenger_count):
    connection = get_db_connection()

    try:
        connection.start_transaction()

        cursor = connection.cursor(dictionary=True)

        # Get schedule details and lock the row
        query = """
            SELECT
                schedule_id,
                price,
                available_capacity,
                status
            FROM schedules
            WHERE schedule_id = %s
            FOR UPDATE
        """

        cursor.execute(query, (schedule_id,))
        schedule = cursor.fetchone()

        if not schedule:
            connection.rollback()
            return {
                "success": False,
                "message": "Schedule not found"
            }

        if schedule["status"] != "AVAILABLE":
            connection.rollback()
            return {
                "success": False,
                "message": "This schedule is not available"
            }

        if schedule["available_capacity"] < passenger_count:
            connection.rollback()
            return {
                "success": False,
                "message": "Not enough seats available"
            }

        # Calculate total amount
        total_amount = schedule["price"] * passenger_count

        # Generate booking reference
        booking_reference = "GT" + uuid.uuid4().hex[:10].upper()

        # Create booking
        insert_query = """
            INSERT INTO bookings
            (
                user_id,
                schedule_id,
                booking_reference,
                total_amount,
                booking_status
            )
            VALUES (%s, %s, %s, %s, 'CONFIRMED')
        """

        cursor.execute(
            insert_query,
            (
                user_id,
                schedule_id,
                booking_reference,
                total_amount
            )
        )

        booking_id = cursor.lastrowid

        # Reduce available capacity
        update_query = """
            UPDATE schedules
            SET available_capacity = available_capacity - %s
            WHERE schedule_id = %s
        """

        cursor.execute(
            update_query,
            (passenger_count, schedule_id)
        )

        connection.commit()

        cursor.close()

        return {
            "success": True,
            "message": "Booking created successfully",
            "booking_id": booking_id,
            "booking_reference": booking_reference,
            "schedule_id": schedule_id,
            "passenger_count": passenger_count,
            "total_amount": float(total_amount),
            "booking_status": "CONFIRMED"
        }

    except Exception as e:
        connection.rollback()

        return {
            "success": False,
            "message": str(e)
        }

    finally:
        connection.close()