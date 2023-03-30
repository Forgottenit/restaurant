// function showModal(title, body, actionText, actionUrl, actionClass = 'btn-danger', deleteUrl) {
//     $('#genericModalLabel').text(title);
//     $('#genericModal .modal-body').text(body);
//     $('#genericModalAction').attr('href', actionUrl).text(actionText).removeClass().addClass(`btn ${actionClass}`);
//     $('#genericModal').modal('show');
//     $('#genericModal .modal-footer #genericModalAction').attr('href', actionUrl).text(actionText).removeClass().addClass(`btn ${actionClass}`);
//     $('#genericModal .modal-footer #confirmCancelReservation').attr('href', deleteUrl);
// }

// $(document).ready(function () {
//     // Show the modal cancel reservation button clicked
//     $('.cancel-reservation-btn').click(function (e) {
//         e.preventDefault();
//         let deleteUrl = $(this).data('delete-url');
//         console.log(deleteUrl); // Check deleteUrl value
//         showModal(
//             'Cancel Reservation',
//             'Are you sure you want to cancel this reservation?',
//             'Delete Reservation',
//             deleteUrl,
//             'btn-danger',
//             deleteUrl // Pass deleteUrl directly to showModal function
//         );
//     });

//     // Confirm cancel reservation and submit form
//     $('#confirmCancelReservation').click(function (e) {
//         e.preventDefault();
//         $('form').attr('action', $(this).attr('href')).unbind('submit').submit();
//     });
// });