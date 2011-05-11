username_changed = false;

$(function(){
    //$('#join').validate('/accounts/join/validate/', {type: 'ul'});
    //$('#settings').validate('/accounts/settings/validate/', {type: 'ul'});
    //$('#password_change').validate('/accounts/password-change/validate/', {type: 'ul'});
    
    $('#join #id_username').change(function() {
        username_changed = true
    });
    
    $('#join #id_full_name').keyup(function() {
        if (!username_changed) {
            $('#join #id_username').val(URLify($(this).val(), 50));
        }
    });
});