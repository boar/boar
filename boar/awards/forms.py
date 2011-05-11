from boar.awards.models import Vote, Nominee
from django import forms
from django.utils.safestring import mark_safe

class NomineesField(forms.ModelChoiceField):
    def label_from_instance(self, obj):
        if obj.link:
            return mark_safe('<a href="%s">%s</a>' % (obj.link, obj.name))
        return obj.name

class VoteForm(forms.Form):
    def __init__(self, ceremony, user, *args, **kwargs):
        super(VoteForm, self).__init__(*args, **kwargs)
        self.ceremony = ceremony
        self.user = user
        for award in self.ceremony.awards.all():
            nominees = award.nominees.all()
            if nominees:
                self.fields[unicode(award.pk)] = NomineesField(
                    queryset=nominees,
                    widget=forms.RadioSelect,
                    label=award.name,
                    empty_label='Abstain',
                    required=False,
                )
        
    def save(self):
        for field, value in self.cleaned_data.items():
            if value:
                Vote.objects.create(
                    user=self.user,
                    nominee=value,
                )