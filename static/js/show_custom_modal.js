function showModal(options) {
    const modal = document.getElementById('customModal');
    const modalTitle = modal.querySelector('.modal-title');
    const modalBody = modal.querySelector('.modal-body');
    const modalAction = modal.querySelector('#customModalAction');

    modalTitle.textContent = options.title || 'Message';
    modalBody.innerHTML = options.body || '';
    modalAction.textContent = options.actionText || 'Close';
    modalAction.classList.add(options.actionClass || 'btn-secondary');

    modalAction.addEventListener('click', function (event) {
        event.preventDefault();
        if (options.actionCallback) {
            options.actionCallback();
        }
        const customModal = bootstrap.Modal.getInstance(modal);
        customModal.hide();
    });

    const customModal = new bootstrap.Modal(modal);
    customModal.show();
}