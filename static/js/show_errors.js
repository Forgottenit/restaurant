document.addEventListener("DOMContentLoaded", function () {
    let errorsElement = document.getElementById('form-errors');
    if (errorsElement) {
        let errors = JSON.parse(errorsElement.textContent);
        let errorMessages = "";

        for (const field in errors) {
            for (const message of errors[field]) {
                errorMessages += "<p>" + message.message + "</p>";
            }
        }

        showModal({
            title: "Sorry...",
            body: errorMessages,
            actionText: "OK",
            actionClass: "btn-secondary",
        });
    }
});