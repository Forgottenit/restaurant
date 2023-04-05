$(document).ready(function () {
    // Show the custom modal when the cancel reservation button is clicked
    $('.cancel-reservation-btn').click(function (e) {
        e.preventDefault();
        let deleteUrl = $(this).data('delete-url');

        showModal({
            title: 'Cancel Reservation',
            body: 'Are you sure you want to cancel this reservation?',
            actionText: 'Confirm Cancellation',
            actionClass: 'btn-danger',
            actionCallback: function () {
                // Perform the delete action by navigating to the delete URL
                window.location.href = deleteUrl;
            }
        });
    });
});