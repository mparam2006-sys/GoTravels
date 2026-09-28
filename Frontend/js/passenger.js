const bookingData = JSON.parse(
    localStorage.getItem("bookingData")
);

const passengerContainer =
    document.getElementById("passengerContainer");

const passengerForm =
    document.getElementById("passengerForm");

const message =
    document.getElementById("message");


if (!bookingData || !bookingData.booking_id) {

    message.textContent =
        "Booking information not found.";

    passengerForm.style.display = "none";

} else {

    const passengerCount =
        bookingData.passenger_count || 1;


    for (let i = 1; i <= passengerCount; i++) {

        const passengerDiv =
            document.createElement("div");

        passengerDiv.className = "passenger";

        passengerDiv.innerHTML = `

            <h3>Passenger ${i}</h3>

            <label>
                Full Name
            </label>

            <input
                type="text"
                class="full_name"
                placeholder="Enter full name"
                required
            >


            <label>
                Age
            </label>

            <input
                type="number"
                class="age"
                min="1"
                placeholder="Enter age"
                required
            >


            <label>
                Gender
            </label>

            <select class="gender" required>

                <option value="">
                    Select Gender
                </option>

                <option value="MALE">
                    Male
                </option>

                <option value="FEMALE">
                    Female
                </option>

                <option value="OTHER">
                    Other
                </option>

            </select>


            <label>
                ID Type
            </label>

            <select class="id_type" required>

                <option value="">
                    Select ID Type
                </option>

                <option value="AADHAAR">
                    Aadhaar
                </option>

                <option value="PASSPORT">
                    Passport
                </option>

                <option value="PAN">
                    PAN Card
                </option>

                <option value="DRIVING_LICENSE">
                    Driving License
                </option>

            </select>


            <label>
                ID Number
            </label>

            <input
                type="text"
                class="id_number"
                placeholder="Enter ID number"
                required
            >

        `;

        passengerContainer.appendChild(passengerDiv);
    }
}


passengerForm.addEventListener(
    "submit",
    async function (event) {

        event.preventDefault();


        if (!bookingData || !bookingData.booking_id) {
            return;
        }


        const passengers = [];


        const passengerDivs =
            document.querySelectorAll(".passenger");


        passengerDivs.forEach(function (div) {

            const fullName =
                div.querySelector(".full_name").value;

            const age =
                parseInt(
                    div.querySelector(".age").value
                );

            const gender =
                div.querySelector(".gender").value;

            const idType =
                div.querySelector(".id_type").value;

            const idNumber =
                div.querySelector(".id_number").value;


            passengers.push({

                full_name: fullName,

                age: age,

                gender: gender,

                id_type: idType,

                id_number: idNumber

            });

        });


        try {

            const response = await fetch(
                `http://127.0.0.1:8000/passengers/${bookingData.booking_id}`,
                {
                    method: "POST",

                    headers: {
                        "Content-Type": "application/json"
                    },

                    body: JSON.stringify({
                        passengers: passengers
                    })
                }
            );


            const data = await response.json();

            console.log(data);


            if (!response.ok) {

                message.textContent =
                    data.detail || "Failed to add passengers.";

                return;
            }


            localStorage.setItem(
                "passengerData",
                JSON.stringify(data)
            );


            window.location.href =
                "payment.html";


        } catch (error) {

            console.error(error);

            message.textContent =
                "Could not connect to GoTravels server.";
        }

    }
);