function slideCallback(text) {
    date = text.split(' ');
    $('#cloud').load('/'+section+'/topics/'+date[1]+'/'+date[0].toLowerCase()+'/?ajax');
}

$(function() {
    var month = $('select#month')
    month.hide();
    month.selectToUISlider();
    $('body').append('<div id="loading"></div>')
    $('#loading').hide().html('<img src="http://media.theboar.org/static/img/ajax-loader.gif" />');
    $('#loading').ajaxStart(function() {
        $(this).show();
    }).ajaxStop(function() {
        $(this).hide();
    });
    
});