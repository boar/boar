from boar.accounts.models import UserProfile
from boar.facebook_connect.models import FacebookProfile
from boar.mailing_lists.models import MailingList
from django.conf import settings
from django.contrib.auth import login, logout
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
import facebook

class FacebookConnectMiddleware(object):
    def process_request(self, request):
        fb_user = facebook.get_user_from_cookie(
            request.COOKIES,
            settings.FACEBOOK_API_KEY,
            settings.FACEBOOK_SECRET_KEY,
        )
        if fb_user:
            if request.user.is_authenticated():
                try:
                    fbp = FacebookProfile.objects.get(user=request.user)
                except FacebookProfile.DoesNotExist:
                    # Logged into facebook, but logged into site with no 
                    # facebook profile.
                    # TODO: some way of connecting this facebook profile
                    logout(request)
                else:
                    if 'uid' not in fb_user or fbp.uid != fb_user['uid']:
                        logout(request)
                        return HttpResponseRedirect(request.path)
            else:
                graph = facebook.GraphAPI(fb_user['access_token'])
                try:
                    info = graph.get_object('me')
                except facebook.GraphAPIError, e:
                    # Session timed out
                    if e.type == 102:
                        logout(request)
                        return
                    else:
                        raise
                except IOError:
                    # HTTP error, such as 401 Unauthorized
                    logout(request)
                    return
                try:
                    fbp = FacebookProfile.objects.get(uid=fb_user['uid'])
                except FacebookProfile.DoesNotExist:
                    # Logged into facebook, but no user exists on the site
                    user_profile = UserProfile.objects.create_from_name(
                        info['name']
                    )
                    user_profile.user.email = info['email']
                    user_profile.user.save()
                    fbp = FacebookProfile.objects.create(
                        user=user_profile.user,
                        uid=fb_user['uid'],
                    )
                    fbp.user.backend = 'django.contrib.auth.backends.ModelBackend'
                    login(request, fbp.user)
                    for ml in MailingList.objects.filter(
                            default_for_new_users=True):
                        ml.subscribers.add(user_profile.user)
                else:
                    # Simulate authenticate()
                    fbp.user.backend = 'django.contrib.auth.backends.ModelBackend'
                    login(request, fbp.user)
        else:
            if request.user.is_authenticated():
                try:
                    fbp = FacebookProfile.objects.get(user=request.user)
                except FacebookProfile.DoesNotExist:
                    pass
                else:
                    # Logged into an account with a facebook profile but with 
                    # no facebook session
                    logout(request)
        
    
