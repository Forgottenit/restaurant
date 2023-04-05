function showModal(options) {
    // Set the modal elements based on the options
    $('#customModalLabel').text(options.title);
    $('#customModal .modal-body').text(options.body);
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

        showModal({
            title: 'Confirm Booking',
            body: 'Are you sure you want to confirm this booking?',
            actionText: 'Confirm Booking',
            actionClass: 'btn-primary',
            actionCallback: function () {
                form.submit(); // Submit the form
            }
        });
    });
});