import datetime
from django.shortcuts import render_to_response
from django import template
from django.http import Http404, HttpResponseRedirect
from boar.awards.forms import VoteForm
from boar.awards.models import Ceremony, Vote

def get_ceremony():
    try:
        return Ceremony.objects.filter(
            start_date__lte=datetime.datetime.now()).order_by('-start_date')[0]
    except IndexError:
        raise Http404('No open ceremonies!')

def ceremony_detail(request):
    ceremony = get_ceremony()
    if ceremony.end_date and ceremony.end_date < datetime.datetime.now():
        return render_to_response('awards/ceremony_closed.html', {
            'ceremony': ceremony,
        }, context_instance=template.RequestContext(request))
    if request.user.is_authenticated():
        if request.method == 'POST':
            form = VoteForm(ceremony, request.user, request.POST, label_suffix='')
            if form.is_valid():
                form.save()
                return HttpResponseRedirect('/awards/thanks/')
        else:
            form = VoteForm(ceremony, request.user, label_suffix='')
    else:
        form = None
    return render_to_response('awards/ceremony_detail.html', {
        'ceremony': ceremony,
        'form': form
    }, context_instance=template.RequestContext(request))

def ceremony_voted(request):
    return render_to_response('awards/ceremony_voted.html', {
        'ceremony': get_ceremony(),
    }, context_instance=template.RequestContext(request))
