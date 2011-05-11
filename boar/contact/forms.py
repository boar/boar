from django import forms
from django.conf import settings
from django.core.mail import send_mail
from django.template import loader
from django.template import RequestContext
from django.contrib.sites.models import Site

class ContactForm(forms.Form):
    subject_template_name = 'contact/email_subject.txt'
    template_name = 'contact/email.txt'
    
    subject = forms.CharField(max_length=200)
    message = forms.CharField(widget=forms.Textarea())
    
    def __init__(self, data=None, files=None, request=None, email=None, *args, **kwargs):
        super(ContactForm, self).__init__(data=data, files=files, *args, **kwargs)
        self.request = request
        self.email = email
    
    def save(self, fail_silently=False):
        """
        Build and send the email message.
        
        """
        send_mail(subject='Boar Website: %s' % self.cleaned_data['subject'],
                  message='Message sent from the Boar website by %s: \n\n%s' % (self.request.user.username, self.cleaned_data['message']),
                  from_email=self.request.user.email,
                  recipient_list=[self.email],
                  fail_silently=fail_silently)
    
            