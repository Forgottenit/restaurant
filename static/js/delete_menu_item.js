$(document).ready(function () {
    // Show the custom modal when the cancel reservation button is clicked
    $('.delete-menu-btn').click(function (e) {
        e.preventDefault();
        let deleteUrl = $(this).data('delete-url');

        showModal({
            title: 'Delete Menu Item',
            body: 'Are you sure you want to Delete this Item?',
            actionText: 'Confirm Deletion',
            actionClass: 'btn-danger',
            actionCallback: function () {
                // Perform the delete action by navigating to the delete URL
                window.location.href = deleteUrl;
            }
        });
    });
});