function showModal(options) {
    // Display customModal
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

    // Show the Modal
    $('#customModal').modal('show');
}