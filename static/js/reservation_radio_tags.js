// Function to target Radio Tags to remove active class for CSS styling

$(document).ready(function () {
    $('input[type="radio"][name="time"]').on('change', function () {
        $('.btn-radio').removeClass('active');
        $(this).parent().addClass('active');
    });
});