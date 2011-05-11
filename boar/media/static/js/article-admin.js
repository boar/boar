$(function() {
    $('#id_tone').change(function() {
        $('#id_tone option').each(function() {
            var elem = $('#id_'+$(this).val()+'_metadata-0-id')
                .parent().parent();
            if ($(this).attr('selected')) {
                elem.show();
            }
            else {
                elem.hide();
            }
        });
    }).change();
});

