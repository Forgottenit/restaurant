function showModal(options) {
    // Set the modal elements based on the options
    $('#customModalLabel').text(options.title);
    $('#customModal .modal-body').html(options.body);
    $('#customModalAction')
        .text(options.actionText)
        .addClass(options.actionClass)
        .off('click')
        .on('click', function (event) {
            event.preventDefault();
            if (options.actionCallback) {
                options.actionCallback();
            }
            $('#customModal').modal('hide');
        });

    // Display the modal
    $('#customModal').modal('show');
}

$(document).ready(function () {
    // Intercept the form submit event
    $('.reservation-form').submit(function (e) {
        e.preventDefault();
        const form = this;
        const name = $('#id_name').val();
        const email = $('#id_email').val();
        const date = $('#id_date').val();
        const time = $('#id_time').val();
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
                form.submit(); // Submit the form
            }
        });
    });
});