const searchForm = document.querySelector("form");

searchForm.addEventListener("submit", async function (event) {
    event.preventDefault();

    const fromCity = document.getElementById("from_city").value.trim();
    const toCity = document.getElementById("to_city").value.trim();
    const travelDate = document.getElementById("travel_date").value;
    const serviceType = document.getElementById("service_type").value;

    if (!fromCity || !toCity || !travelDate) {
        alert("Please fill in From, To and Date.");
        return;
    }

    let url =
        `http://127.0.0.1:8000/search?from_city=${encodeURIComponent(fromCity)}` +
        `&to_city=${encodeURIComponent(toCity)}` +
        `&travel_date=${encodeURIComponent(travelDate)}`;

    if (serviceType && serviceType !== "ALL") {
        url += `&service_type=${encodeURIComponent(serviceType)}`;
    }

    try {
        const response = await fetch(url);

        const data = await response.json();

        console.log("Search response:", data);

        if (!response.ok) {
            alert(data.detail || "Search failed.");
            return;
        }

        localStorage.setItem(
            "searchResults",
            JSON.stringify(data.results)
        );

        localStorage.setItem(
            "searchFrom",
            fromCity
        );

        localStorage.setItem(
            "searchTo",
            toCity
        );

        localStorage.setItem(
            "searchDate",
            travelDate
        );

        window.location.href = "results.html";

    } catch (error) {
        console.error("Search error:", error);

        alert(
            "Could not connect to GoTravels server. " +
            "Please make sure the FastAPI server is running."
        );
    }
});