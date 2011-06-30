from django import forms

class ThumbInlineForm(forms.ModelForm):
    left = forms.IntegerField(widget=forms.HiddenInput)
    right = forms.IntegerField(widget=forms.HiddenInput)
    top = forms.IntegerField(widget=forms.HiddenInput)
    bottom = forms.IntegerField(widget=forms.HiddenInput)
        
    class Media:
        js = (
            'js/src/jquery-1.3.2.min.js',
            'js/jquery.imgareaselect-0.6.2.min.js',
        )
