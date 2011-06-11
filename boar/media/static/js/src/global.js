Hyphenator.config({
    remoteloading: false,
    intermediatestate : 'visible',
    selectorfunction: function () {
    	return $('.article-column p');
    }
});
Hyphenator.run();

$.fn.spinnyThing = function() {
    this.html('<img src="'+boar.MEDIA_URL+'static/img/ajax-loader.gif" />');
}

$(function() {
    var s = $("#search input");
    if (s.val() == '') {
        s.labelify({labelledClass: "label"});
    }
    
    $('#sections li a:not(.active)').map(function() {
        $(this).addClass('active');
        var bg = $(this).css('background-color');
        var text = $(this).css('color');
        $(this).removeClass('active').hover(function(){
            $(this).stop().animate({ backgroundColor: bg, color: text }, 120);
        }, function() {
            $(this).stop().animate({ backgroundColor: "#000", color: "#FFF" }, 120);
        });
    });
    
    $('#messages').slideDown(500);
    
    // Comments
    var comments = $('#comments');
    comments.find('div.reply a').show().each(function() {
        $(this).click(function() {
                $(this).parent().parent().
                    children(".comment-form").slideToggle(500);
            return false;
        });
    });
    comments.find('.new-thread').show();
    comments.find('.comment-form').submit(function() {
        var form = this;
        FB.getLoginStatus(function(response) {
            if (response.session) {
                form.submit();
            }
            else {
                FB.login(function(response) {
                    if (response.session) {
                        form.submit();
                    }
                }, {'perms': 'email'});
            }
        });
        return false;
    });
    
    // Facebook
    $.getScript(
        document.location.protocol+'//connect.facebook.net/en_US/all.js',
    function() {
        var userBar = $('#user-bar');
        FB.init({
            appId: boar.facebookAppId,
            status: true,
            cookie: true,
            xfbml: true
        });
        var updateUserBar = function(response) {
            if (response.session) {
                $.getJSON('/accounts/user-data/', function(data) {
                    if (data.user) {
                        userBar.html(
                            '<li><a href="/users/'+data.user.username+'/"><img src="'+boar.MEDIA_URL+'static/img/facebook-icon.png" alt="Logged in with Facebook" width="18" height="18" /></a></li>'+
                            '<li><a href="/users/'+data.user.username+'/">'+data.user.first_name+' '+data.user.last_name+'</a></li>'
                        );
                    }
                    // If the server didn't find a user for whatever reason,
                    // don't explode
                    else {
                        FB.api('/me', function(response) {
                            userBar.html(
                                '<li><img src="'+boar.MEDIA_URL+'static/img/facebook-icon.png" alt="Logged in with Facebook" width="18" height="18" /></li>'+
                                '<li>'+response.name+'</li>'
                            );
                        });
                    }
                    
                    userBar.append('<li><a href="/accounts/">Mailing lists</a></li>');
                    if (data.user && data.user.is_staff) {
                        userBar.append('<li><a href="/admin/">Admin</a></li>');
                    }
                    userBar.append(
                        $('<li><a href="#">Sign out</a></li>').click(function() {
                            FB.logout();
                            return false;
                        })
                    );
                });
            }
            else {
                userBar.html('<fb:login-button perms="email" length="long"></fb:login-button>');
                FB.XFBML.parse(userBar[0]);
            }
        }
        FB.Event.subscribe('auth.sessionChange', function(response) {
            if (boar.refreshOnSessionChange) {
                window.location = window.location;
                return;
            }
            updateUserBar(response);
        });
        FB.getLoginStatus(updateUserBar);

        // Recommendations block
        var archiveBlock = $('#home .archive-block');
        if (archiveBlock.length) {
            archiveBlock.after(
                '<div class="block">'+
                    '<h3>Recommendations</h3>'+
                    '<fb:recommendations width="284" height="500" header="false" border_color="#FFF"></fb:recommendations>'+
                '</div>'
            );
            FB.XFBML.parse(archiveBlock[0]);
        }

    });

    
});

