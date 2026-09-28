from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from schemas import (
    UserCreate,
    PassengerList
)

from models import (
    create_user,
    login_user,
    get_all_travel_services,
    search_travel_services
)

from booking import create_booking
from passenger import add_passengers
from payment import process_payment
from my_bookings import get_user_bookings
from cancellation import cancel_booking


app = FastAPI(title="GoTravels API")


# Allow frontend to communicate with FastAPI
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def home():
    return {
        "message": "Welcome to GoTravels API"
    }


@app.post("/register")
def register_user(user: UserCreate):

    user_id = create_user(
        user.full_name,
        user.email,
        user.phone,
        user.password
    )

    return {
        "message": "User registered successfully",
        "user_id": user_id
    }


@app.post("/login")
def login(email: str, password: str):

    user = login_user(email, password)

    if not user:
        raise HTTPException(
            status_code=401,
            detail="Invalid email or password"
        )

    return {
        "message": "Login successful",
        "user": user
    }


@app.get("/travel-services")
def travel_services():

    services = get_all_travel_services()

    return {
        "services": services
    }


@app.get("/search")
def search(
    from_city: str,
    to_city: str,
    travel_date: str,
    service_type: str | None = None
):

    results = search_travel_services(
        from_city,
        to_city,
        travel_date,
        service_type
    )

    return {
        "results": results
    }


@app.post("/book")
def book(
    user_id: int,
    schedule_id: int,
    passenger_count: int
):

    if passenger_count < 1:
        raise HTTPException(
            status_code=400,
            detail="Passenger count must be at least 1"
        )

    result = create_booking(
        user_id,
        schedule_id,
        passenger_count
    )

    if not result["success"]:
        raise HTTPException(
            status_code=400,
            detail=result["message"]
        )

    return result


@app.post("/passengers/{booking_id}")
def add_booking_passengers(
    booking_id: int,
    passenger_data: PassengerList
):

    if len(passenger_data.passengers) < 1:
        raise HTTPException(
            status_code=400,
            detail="At least one passenger is required"
        )

    passengers = []

    for passenger in passenger_data.passengers:

        if passenger.age < 1:
            raise HTTPException(
                status_code=400,
                detail="Passenger age must be greater than 0"
            )

        if passenger.gender.upper() not in [
            "MALE",
            "FEMALE",
            "OTHER"
        ]:
            raise HTTPException(
                status_code=400,
                detail="Gender must be MALE, FEMALE or OTHER"
            )

        passengers.append({
            "full_name": passenger.full_name,
            "age": passenger.age,
            "gender": passenger.gender.upper(),
            "id_type": passenger.id_type,
            "id_number": passenger.id_number
        })

    result = add_passengers(
        booking_id,
        passengers
    )

    if not result["success"]:
        raise HTTPException(
            status_code=400,
            detail=result["message"]
        )

    return result


@app.post("/payment/{booking_id}")
def payment(
    booking_id: int,
    payment_method: str
):

    allowed_methods = [
        "CARD",
        "NET_BANKING",
        "UPI",
        "WALLET"
    ]

    if payment_method.upper() not in allowed_methods:
        raise HTTPException(
            status_code=400,
            detail="Invalid payment method"
        )

    result = process_payment(
        booking_id,
        payment_method
    )

    if not result["success"]:
        raise HTTPException(
            status_code=400,
            detail=result["message"]
        )

    return result


@app.get("/my-bookings/{user_id}")
def my_bookings(user_id: int):

    bookings = get_user_bookings(user_id)

    return {
        "user_id": user_id,
        "bookings": bookings
    }


@app.post("/cancel/{booking_id}")
def cancel(
    booking_id: int,
    reason: str = "User requested cancellation"
):

    result = cancel_booking(
        booking_id,
        reason
    )

    if not result["success"]:
        raise HTTPException(
            status_code=400,
            detail=result["message"]
        )

    return result