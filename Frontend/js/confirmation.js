const bookingData = JSON.parse(
    localStorage.getItem("bookingData")
);

const paymentData = JSON.parse(
    localStorage.getItem("paymentData")
);


if (bookingData) {

    document.getElementById("bookingId").textContent =
        bookingData.booking_id || "Not available";

    document.getElementById("totalAmount").textContent =
        bookingData.total_amount || "Not available";

} else {

    document.getElementById("bookingId").textContent =
        "Not available";

    document.getElementById("totalAmount").textContent =
        "Not available";
}


if (paymentData) {

    document.getElementById("paymentStatus").textContent =
        paymentData.payment_status ||
        paymentData.status ||
        "Successful";

} else {

    document.getElementById("paymentStatus").textContent =
        "Successful";
}