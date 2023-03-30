$(document).ready(function () {
    // Show the modal cancel reservation button clicked

    $('.cancel-reservation-btn').click(function (e) {
        e.preventDefault();
        let deleteUrl = $(this).data('delete-url');
        $('#confirmCancelReservation').attr('href', deleteUrl);
        $('#cancelReservationModal').modal('show');
    });

    // Close the modal and delete reservation
    $('#confirmCancelReservation').click(function () {
        $('#cancelReservationModal').modal('hide');
    });
});