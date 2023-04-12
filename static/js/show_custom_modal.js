// function showModal(options) {
//     // Display customModal
//     console.log('showModal Display called');
//     $('#customModalLabel').text(options.title);
//     $('#customModal .modal-body').html(options.body);
//     $('#customModalAction')
//         .text(options.actionText)
//         .addClass(options.actionClass)
//         .off('click')
//         .on('click', function (event) {
//             event.preventDefault();
//             if (options.actionCallback) {
//                 options.actionCallback();
//             }
//             $('#customModal').modal('hide');
//         });

//     // Show the Modal
//     $('#customModal').modal('show');
// }

// function showModal(options) {
//     const modal = document.getElementById('customModal');
//     const modalLabel = modal.querySelector('.modal-title');
//     const modalBody = modal.querySelector('.modal-body');
//     const modalAction = modal.querySelector('#customModalAction');

//     modalLabel.textContent = options.title || 'Message';
//     modalBody.innerHTML = options.body || '';
//     modalAction.textContent = options.actionText || 'Close';
//     modalAction.classList.add(options.actionClass || 'btn-secondary');

//     modalAction.addEventListener('click', function (event) {
//         event.preventDefault();
//         if (options.actionCallback) {
//             options.actionCallback();
//         }
//         $('#customModal').modal('hide');
//     });

//     $('#customModal').modal('show');
// }

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





// function showModal(options) {
//     const modal = document.getElementById('customModal');
//     const modalLabel = modal.querySelector('.modal-title');
//     const modalBody = modal.querySelector('.modal-body');
//     const modalAction = modal.querySelector('#customModalAction');

//     const errorMessage = document.getElementById('error-message').textContent;
//     console.log(errorMessage);
//     if (errorMessage) {
//         modalLabel.textContent = options.title || 'Error';
//         modalBody.innerHTML = errorMessage;
//         modalAction.textContent = 'Close';
//         modalAction.classList.add('btn-secondary');
//     } else {
//         modalLabel.textContent = options.title || 'Message';
//         modalBody.innerHTML = options.body || '';
//         modalAction.textContent = options.actionText || 'Close';
//         modalAction.classList.add(options.actionClass || 'btn-secondary');

//         modalAction.addEventListener('click', function (event) {
//             event.preventDefault();
//             if (options.actionCallback) {
//                 options.actionCallback();
//             }
//             $('#customModal').modal('hide');
//         });
//     }

//     $('#customModal').modal('show');
// }