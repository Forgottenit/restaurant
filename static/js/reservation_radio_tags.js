jQuery(document).ready(function () {
    jQuery('input[type="radio"][name="time"]').on('change', function () {
        jQuery('.btn-radio').removeClass('active');
        jQuery(this).parent().addClass('active');
    });
});