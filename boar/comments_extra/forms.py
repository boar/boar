from threadedcomments.forms import ThreadedCommentForm

class NoEmailThreadedCommentForm(ThreadedCommentForm):
    def __init__(self, *args, **kwargs):
        super(NoEmailThreadedCommentForm, self).__init__(*args, **kwargs)
        self.fields['email'].required = False

