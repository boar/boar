function updateCount() {
    var val = $('#summary').attr('value');
    if (val)
        $('#charcount').html(val.length);
    else
        $('#charcount').html('0');
}


$(document).ready(function()    {
    $('.markitup').markItUp(mySettings);
    $('#summary').after('<p><span id="charcount">0</span> characters</p>');
    updateCount();
    $('#summary').change(updateCount);
    $('#summary').keyup(updateCount);
});


