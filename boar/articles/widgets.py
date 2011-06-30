from django import forms

class MarkItUpWidget(forms.Textarea):
    def __init__(self, *args, **kwargs):
        super(MarkItUpWidget, self).__init__(attrs={'class': 'markitup'}, *args, **kwargs)
    
    class Media:
        js = (
            'js/src/jquery-1.3.2.min.js',
            'js/markitup/jquery.markitup.pack.js',
            'js/markitup/sets/markdown/set.js',
            'js/admin_markitup.js',
        )
        css = {
            'screen': (
                'js/markitup/skins/simple/style.css',
                'js/markitup/sets/markdown/style.css',
            )
        }

