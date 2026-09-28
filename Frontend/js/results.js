const resultsContainer = document.getElementById("results");

const searchResults = JSON.parse(
    localStorage.getItem("searchResults")
);

if (!searchResults || searchResults.length === 0) {

    resultsContainer.innerHTML = `
        <p class="no-results">
            No travel options found.
        </p>
    `;

} else {

    resultsContainer.innerHTML = "";

    searchResults.forEach(service => {

        const card = document.createElement("div");

        card.className = "travel-card";

        card.innerHTML = `
            <h2>${service.service_name}</h2>

            <p>
                <strong>Type:</strong>
                ${service.service_type}
            </p>

            <p>
                <strong>Provider:</strong>
                ${service.provider_name}
            </p>

            <p>
                <strong>Service Number:</strong>
                ${service.service_number}
            </p>

            <p>
                <strong>From:</strong>
                ${service.departure_city}
            </p>

            <p>
                <strong>To:</strong>
                ${service.arrival_city}
            </p>

            <p>
                <strong>Departure:</strong>
                ${service.departure_datetime}
            </p>

            <p>
                <strong>Arrival:</strong>
                ${service.arrival_datetime}
            </p>

            <p>
                <strong>Available Seats:</strong>
                ${service.available_capacity}
            </p>

            <p class="price">
                ₹${service.price}
            </p>

            <button class="book-btn"
                onclick="bookService(${service.schedule_id})">
                Book Now
            </button>
        `;

        resultsContainer.appendChild(card);
    });
}


function bookService(scheduleId) {

    localStorage.setItem(
        "selectedScheduleId",
        scheduleId
    );

    window.location.href = "booking.html";
}