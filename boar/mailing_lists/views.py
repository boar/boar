from boar.mailing_lists.models import MailingList
from boar.mailing_lists.tokens import default_token_generator
from django import template
from django.contrib.auth.models import User
from django.http import Http404
from django.shortcuts import get_object_or_404, render_to_response

def unsubscribe(request, user_id, mailing_list_id, token):
    user = get_object_or_404(User, pk=user_id)
    mailing_list = get_object_or_404(MailingList, pk=mailing_list_id)
    if not default_token_generator.check_token(user, mailing_list, token):
        raise Http404('Invalid token')
    if request.method == 'POST':
        if mailing_list.subscribers.filter(pk=user.pk):
            mailing_list.subscribers.remove(user)
        return render_to_response('mailing_lists/unsubscribe_success.html', {
            'user': user,
            'mailing_list': mailing_list,
        }, context_instance=template.RequestContext(request))
    else:
        return render_to_response('mailing_lists/unsubscribe_confirm.html', {
            'user': user,
            'mailing_list': mailing_list,
        }, context_instance=template.RequestContext(request))
