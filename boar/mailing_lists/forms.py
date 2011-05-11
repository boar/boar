from boar.mailing_lists.models import MailingList
from django import forms
from django.utils.html import conditional_escape
from django.utils.encoding import force_unicode
from django.utils.safestring import mark_safe
from itertools import chain
from typogrify.templatetags.typogrify import typogrify

class MailingListsWidget(forms.CheckboxSelectMultiple):
    def render(self, name, value, attrs=None, choices=()):
        mailing_lists = dict((ml.id, ml) for ml in MailingList.objects.all())
        if value is None:
            value = []
        has_id = attrs and 'id' in attrs
        final_attrs = self.build_attrs(attrs, name=name)
        output = [u'<ol>']
        # Normalize to strings
        str_values = set([force_unicode(v) for v in value])
        for i, (option_value, option_label) in enumerate(chain(self.choices, choices)):
            # If an ID attribute was given, add a numeric index as a suffix,
            # so that the checkboxes don't all have the same ID attribute.
            if has_id:
                final_attrs = dict(final_attrs, id='%s_%s' % (attrs['id'], i))
                label_for = u' for="%s"' % final_attrs['id']
            else:
                label_for = ''
 
            cb = forms.CheckboxInput(final_attrs, check_test=lambda value: value in str_values)
            ml = mailing_lists[option_value]
            output.append(u'<li>%s <div class="label"><label%s>%s</label> <p class="donthyphenate">%s</p></div></li>' % (
                cb.render(name, force_unicode(option_value)),
                label_for,
                conditional_escape(typogrify(ml.name)),
                conditional_escape(typogrify(ml.description)),
            ))
        output.append(u'</ol>')
        return mark_safe(u'\n'.join(output))
    

class MailingListsForm(forms.Form):
    mailing_lists = forms.ModelMultipleChoiceField(
        queryset=MailingList.objects.filter(is_visible=True),
        widget=MailingListsWidget,
        required=False,
    )

