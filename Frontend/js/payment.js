const form = document.querySelector("form");

form.addEventListener("submit", async function (event) {
    event.preventDefault();

    // Get booking ID created on the booking page
    const bookingId =
        localStorage.getItem("bookingId") ||
        localStorage.getItem("booking_id");

    if (!bookingId) {
        alert("Booking ID is missing.");
        return;
    }

    // Find all passenger input sections
    const passengerCards = document.querySelectorAll(
        ".passenger-card, .passenger, .passenger-box"
    );

    const passengers = [];

    // If passenger cards exist
    if (passengerCards.length > 0) {

        passengerCards.forEach(function (card) {

            const fullName = card.querySelector(
                '[name="full_name"], #full_name'
            );

            const age = card.querySelector(
                '[name="age"], #age'
            );

            const gender = card.querySelector(
                '[name="gender"], #gender'
            );

            const idType = card.querySelector(
                '[name="id_type"], #id_type'
            );

            const idNumber = card.querySelector(
                '[name="id_number"], #id_number'
            );

            passengers.push({
                full_name: fullName.value,
                age: parseInt(age.value),
                gender: gender.value.toUpperCase(),
                id_type: idType.value,
                id_number: idNumber.value
            });
        });

    } else {

        // Fallback for a single passenger
        const fullName = document.querySelector(
            '[name="full_name"], #full_name'
        );

        const age = document.querySelector(
            '[name="age"], #age'
        );

        const gender = document.querySelector(
            '[name="gender"], #gender'
        );

        const idType = document.querySelector(
            '[name="id_type"], #id_type'
        );

        const idNumber = document.querySelector(
            '[name="id_number"], #id_number'
        );

        if (!fullName || !age || !gender || !idType || !idNumber) {
            alert("Passenger form fields not found.");
            return;
        }

        passengers.push({
            full_name: fullName.value,
            age: parseInt(age.value),
            gender: gender.value.toUpperCase(),
            id_type: idType.value,
            id_number: idNumber.value
        });
    }

    // Basic validation
    for (const passenger of passengers) {

        if (!passenger.full_name.trim()) {
            alert("Please enter passenger name.");
            return;
        }

        if (!passenger.age || passenger.age < 1) {
            alert("Please enter a valid passenger age.");
            return;
        }

        if (!["MALE", "FEMALE", "OTHER"].includes(passenger.gender)) {
            alert("Invalid gender.");
            return;
        }

        if (!passenger.id_number.trim()) {
            alert("Please enter ID number.");
            return;
        }
    }

    const requestData = {
        passengers: passengers
    };

    console.log("Booking ID:", bookingId);
    console.log("Passenger data:", requestData);

    try {

        const response = await fetch(
            `http://127.0.0.1:8000/passengers/${bookingId}`,
            {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify(requestData)
            }
        );

        const data = await response.json();

        console.log("Passenger API response:", data);

        if (!response.ok) {
            alert(data.detail || "Failed to add passenger details.");
            return;
        }

        // Keep booking ID for the payment page
        localStorage.setItem("bookingId", bookingId);

        // Store passenger response if needed later
        localStorage.setItem(
            "passengerData",
            JSON.stringify(data)
        );

        // Go to payment page
        window.location.href = "payment.html";

    } catch (error) {

        console.error("Passenger error:", error);

        alert(
            "Could not connect to GoTravels server. " +
            "Please make sure FastAPI is running."
        );
    }
});