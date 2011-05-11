from boar.accounts.forms import UserForm
from boar.common.response import JsonResponse
from boar.facebook_connect.decorators import login_required
from boar.mailing_lists.forms import MailingListsForm
from boar.uploads.models import Image
from django.contrib.auth import logout
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, Http404
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext

@login_required
def accounts(request, settings_form=None, mailing_lists_form=None):
    if settings_form is None:
        settings_form = UserForm(instance=request.user, label_suffix='', prefix='user_')
    if mailing_lists_form is None:
        mailing_lists_form = MailingListsForm(initial={
            'mailing_lists': [ml.id for ml in request.user.mailing_lists.all()],
        }, prefix='ml_')
    return render_to_response('accounts/settings.html', {
        'settings_form': settings_form,
        'mailing_lists_form': mailing_lists_form,
    }, context_instance=RequestContext(request))


def signout(request):
    logout(request)
    return HttpResponseRedirect(request.REQUEST.get('next', '/'))

@login_required
def settings_form(request):
    if request.method == 'POST':
        user_form = UserForm(request.POST, instance=request.user, label_suffix='', prefix='user_')
        ml_form = MailingListsForm(request.POST, prefix='ml_')
        if user_form.is_valid() and ml_form.is_valid():
            user_form.save()
            if 'mailing_lists' in ml_form.cleaned_data:
                request.user.mailing_lists = ml_form.cleaned_data['mailing_lists']
            else:
                request.user.mailing_lists = []
            request.user.save()
            request.user.message_set.create(message='Your settings have been saved.')
            return HttpResponseRedirect(reverse('accounts'))
        else:
            return accounts(request, settings_form=user_form, mailing_lists_form=ml_form)
    return HttpResponseRedirect(reverse('accounts'))

def image_detail(request, username, image_id):
    user = get_object_or_404(User, username=username)
    try:
        image = Image.objects.published().filter(author=user).get(id=image_id)
    except Image.DoesNotExist:
        raise Http404('Image does not exist.')
    return render_to_response('accounts/user_image_detail.html', {
        'user': user,
        'image': image,
    }, context_instance=RequestContext(request))


def user_data(request):
    d = {}
    if request.user.is_authenticated():
        d['user'] = {}
        for k in ('username', 'first_name', 'last_name', 'is_staff'):
            d['user'][k] = getattr(request.user, k)
    return JsonResponse(d)
