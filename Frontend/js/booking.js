const scheduleId = localStorage.getItem("selectedScheduleId");

const serviceInfo = document.getElementById("serviceInfo");
const bookingForm = document.getElementById("bookingForm");
const message = document.getElementById("message");


if (!scheduleId) {

    serviceInfo.innerHTML = `
        <p>No travel service selected.</p>
    `;

    bookingForm.style.display = "none";

} else {

    const searchResults = JSON.parse(
        localStorage.getItem("searchResults")
    );

    const selectedService = searchResults.find(
        service => service.schedule_id == scheduleId
    );


    if (!selectedService) {

        serviceInfo.innerHTML = `
            <p>Travel service details not found.</p>
        `;

        bookingForm.style.display = "none";

    } else {

        serviceInfo.innerHTML = `
            <h3>${selectedService.service_name}</h3>

            <p>
                <strong>Type:</strong>
                ${selectedService.service_type}
            </p>

            <p>
                <strong>Provider:</strong>
                ${selectedService.provider_name}
            </p>

            <p>
                <strong>Service Number:</strong>
                ${selectedService.service_number}
            </p>

            <p>
                <strong>Route:</strong>
                ${selectedService.departure_city}
                →
                ${selectedService.arrival_city}
            </p>

            <p>
                <strong>Departure:</strong>
                ${selectedService.departure_datetime}
            </p>

            <p>
                <strong>Arrival:</strong>
                ${selectedService.arrival_datetime}
            </p>

            <p>
                <strong>Price per passenger:</strong>
                ₹${selectedService.price}
            </p>

            <p>
                <strong>Available seats:</strong>
                ${selectedService.available_capacity}
            </p>
        `;
    }
}


bookingForm.addEventListener("submit", async function (event) {

    event.preventDefault();

    const userId =
        document.getElementById("user_id").value;

    const passengerCount =
        document.getElementById("passenger_count").value;


    if (!scheduleId) {

        alert("No travel service selected.");
        return;
    }


    if (!userId) {

        alert("Please enter User ID.");
        return;
    }


    if (!passengerCount || passengerCount < 1) {

        alert("Please enter a valid number of passengers.");
        return;
    }


    const url =
        `http://127.0.0.1:8000/book` +
        `?user_id=${encodeURIComponent(userId)}` +
        `&schedule_id=${encodeURIComponent(scheduleId)}` +
        `&passenger_count=${encodeURIComponent(passengerCount)}`;


    try {

        const response = await fetch(url, {
            method: "POST"
        });


        const data = await response.json();

        console.log("Booking response:", data);


        if (!response.ok) {

            message.textContent =
                data.detail || "Booking failed.";

            return;
        }


        // Save complete booking response
        localStorage.setItem(
            "bookingData",
            JSON.stringify(data)
        );


        // Save booking ID separately
        localStorage.setItem(
            "bookingId",
            data.booking_id
        );


        // Save total amount
        if (data.total_amount !== undefined) {

            localStorage.setItem(
                "totalAmount",
                data.total_amount
            );
        }


        console.log(
            "Booking ID:",
            data.booking_id
        );


        // Go to passenger details
        window.location.href = "passenger.html";

    } catch (error) {

        console.error("Booking error:", error);

        message.textContent =
            "Could not connect to GoTravels server.";
    }

});