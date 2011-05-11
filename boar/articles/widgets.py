from django import forms
from django.contrib.admin.widgets import FilteredSelectMultiple
from django.db.models import get_model
from django.utils import simplejson
from django.utils.safestring import mark_safe
from tagging.models import Tag

from boar.articles.models import Article

class AutoCompleteTagInput(forms.TextInput):
    class Media:
        css = {
            'all': ('static/css/jquery.autocomplete.css',)
        }
        js = (
            'static/js/src/jquery-1.3.2.min.js',
            'static/js/jquery.bgiframe.min.js',
            'static/js/jquery.ajaxQueue.js',
            'static/js/jquery.autocomplete.min.js'
        )

    def render(self, name, value, attrs=None):
        output = super(AutoCompleteTagInput, self).render(name, value, attrs)
        page_tags = Tag.objects.usage_for_model(Article)
        tag_list = simplejson.dumps([tag.name for tag in page_tags],
                                    ensure_ascii=False)
        return output + mark_safe(u'''<script type="text/javascript">
            $("#id_%s").autocomplete(%s, {
                width: 150,
                max: 10,
                highlight: false,
                multiple: true,
                multipleSeparator: ", ",
                scroll: true,
                scrollHeight: 300,
                matchContains: true,
                autoFill: true
            });
            </script>''' % (name, tag_list))

class MarkItUpWidget(forms.Textarea):
    def __init__(self, *args, **kwargs):
        super(MarkItUpWidget, self).__init__(attrs={'class': 'markitup'}, *args, **kwargs)
    
    class Media:
        js = (
            'static/js/src/jquery-1.3.2.min.js',
            'static/js/markitup/jquery.markitup.pack.js',
            'static/js/markitup/sets/markdown/set.js',
            'static/js/admin_markitup.js',
        )
        css = {
            'screen': (
                'static/js/markitup/skins/simple/style.css',
                'static/js/markitup/sets/markdown/style.css',
            )
        }
