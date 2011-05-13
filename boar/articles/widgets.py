from django import forms

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

