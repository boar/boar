from django import forms
from django.contrib.auth.models import User

class UserForm(forms.ModelForm):
    full_name = forms.CharField()
    
    def __init__(self, *args, **kwargs):
        super(UserForm, self).__init__(*args, **kwargs)
        self.initial['full_name'] = ('%s %s' % (self.instance.first_name, self.instance.last_name)).strip()
        
    def save(self, *args, **kwargs):
        u = super(UserForm, self).save(*args, **kwargs)
        try:
            u.first_name, u.last_name = self.cleaned_data['full_name'].split(None, 1)
        except ValueError:
            u.first_name, u.last_name = self.cleaned_data['full_name'], ''
        u.save()
        return u
    
    class Meta:
        model = User
        fields = ['full_name', 'email']


