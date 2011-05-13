import datetime
import time

from django import forms
from django.contrib.admin.widgets import FilteredSelectMultiple
from boar.articles.models import Article, Tag
from boar.articles.widgets import MarkItUpWidget

class ArticleAdminModelForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        # Make TagManager act like a ManyToManyField
        if 'initial' not in kwargs:
            kwargs['initial'] = {}
        if kwargs.get('instance', None):
            opts = self._meta.model._meta
            for f in sorted(opts.fields + opts.many_to_many):
                if f.name == 'tags':
                    if kwargs['instance'].pk is None:
                        kwargs['initial'][f.name] = []
                    else:
                        kwargs['initial'][f.name] = [obj.tag.pk for obj in f.value_from_object(kwargs['instance'])]
        super(ArticleAdminModelForm, self).__init__(*args, **kwargs)
        if 'pub_date' in self.initial and isinstance(self.initial['pub_date'], basestring):
            self.initial['pub_date'] =  datetime.datetime(*time.strptime(self.initial['pub_date'], '%Y-%m-%d %H:%M:%S')[:6])


    summary = forms.CharField(required=False, widget=forms.Textarea(attrs={'id': 'summary', 'rows': '5', 'cols': '80'}), help_text=Article._meta.get_field('summary').help_text)
    #body = forms.CharField(widget=forms.Textarea(attrs={'rows': '25', 'cols': '80'}))
    body = forms.CharField(widget=MarkItUpWidget(), help_text=Article._meta.get_field('body').help_text)
    #pub_date = forms.DateTimeField()
    tags = forms.ModelMultipleChoiceField(
        queryset=Tag.objects.all(),
        widget=FilteredSelectMultiple('Tags', False), 
        required=False, 
        help_text="In order of specificness/importance. Tags can be separated by commas <i>or</i> spaces, so if you are using a single tag that is comprised of multiple words, surround it with quotes."
    )
    
    class Meta:
        model = Article


class ArticleArchiveForm(forms.Form):
    def __init__(self, *args, **kwargs):
        qs = kwargs['qs']
        del(kwargs['qs'])
        super(ArticleArchiveForm, self).__init__(*args, **kwargs)
        self.fields['month'].choices = [(d.strftime('%Y-%b').lower(), d.strftime('%B %Y')) for d in qs.dates('pub_date', 'month')]
    
    month = forms.ChoiceField(choices=[])

