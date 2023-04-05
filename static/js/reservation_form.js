$(document).ready(function () {
    // On Submit, Display Modal
    $('.reservation-form').submit(function (e) {
        e.preventDefault();
        const form = this;
        const name = $('#id_name').val();
        const email = $('#id_email').val();
        const date = $('#id_date').val();
        const time = $('input[name="time"]:checked').val();
        const requests = $('#id_special_requests').val();
        const seats = $('#id_party_size').val();

        const bookingDetails = `
            Name: ${name}<br>
            Email: ${email}<br>
            Date: ${date}<br>
            Time: ${time}<br>
            Requests: ${requests}<br>
            Seats: ${seats}
        `;
        showModal({
            title: 'Confirm Booking',
            body: bookingDetails,
            actionText: 'Confirm Booking',
            actionClass: 'btn-primary',
            actionCallback: function () {
                form.submit();
            }
        });
    });
});