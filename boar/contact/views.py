from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, Http404
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext

from boar.articles.models import Position, Section
from boar.contact.forms import ContactForm

class Contact(object):
    template = 'contact/form.html'
    template_not_auth = 'contact/form_not_auth.html'
    form = ContactForm
    
    def __init__(self, template=None):
        if template:
            self.template = template
    
    def __call__(self, request, slug):
        self.request = request
        recipient = self.get_recipient(slug)
        email = self.get_email(recipient)
        name = self.get_name(recipient)
        if not request.user.is_authenticated():
            return render_to_response(self.template_not_auth, {
                'name': name,
            }, context_instance=RequestContext(request))
        if not email:
            raise Http404
        if request.method == 'POST':
            form = self.form(request.POST, request=request, email=email, label_suffix='')
            if form.is_valid():
                form.save()
                return HttpResponseRedirect(reverse('contact_success'))
        else:
            form = self.form(request=request, email=email, label_suffix='')
        return render_to_response(self.template, {
            'recipient': recipient,
            'form': form,
            'name': name,
        }, context_instance=RequestContext(request))
        
    def get_recipient(self, slug):
        raise NotImplementedError
    
    def get_email(self, recipient):
        return recipient.email
    
    def get_name(self, recipient):
        return str(recipient)

class ContactPosition(Contact):
    def get_recipient(self, slug):
        return get_object_or_404(Position, slug=slug)

class ContactSection(Contact):
    def get_recipient(self, slug):
        return get_object_or_404(Section, slug=slug)
    
class ContactUser(Contact):
    def get_recipient(self, slug):
        user = get_object_or_404(User, username=slug)
        if not user.is_staff:
            raise Http404
        return user
    
    def get_name(self, recipient):
        return recipient.get_full_name()
