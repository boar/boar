import re
import string

from django import template
from django.utils.encoding import force_unicode
from django.utils.html import word_split_re, punctuation_re, simple_email_re
from django.utils.http import urlquote
from django.utils.safestring import SafeData, mark_safe

register = template.Library()

@register.filter
def urlify_markdown(text):
    """
    Converts any URLs in text into markdown links.
 
    Works on http://, https://, www. links and links ending in .org, .net or
    .com. Links can have trailing punctuation (periods, commas, close-parens)
    and leading punctuation (opening parens) and it'll still do the right
    thing.
    """
    safe_input = isinstance(text, SafeData)
    words = word_split_re.split(force_unicode(text))
    for i, word in enumerate(words):
        match = None
        if '.' in word or '@' in word or ':' in word:
            match = punctuation_re.match(word)
        if match:
            lead, middle, trail = match.groups()
            # Make URL we want to point to.
            url = None
            if middle.startswith('http://') or middle.startswith('https://'):
                url = urlquote(middle, safe='/&=:;#?+*')
            elif middle.startswith('www.') or ('@' not in middle and \
                    middle and middle[0] in string.ascii_letters + string.digits and \
                    (middle.endswith('.org') or middle.endswith('.net') or middle.endswith('.com'))):
                url = urlquote('http://%s' % middle, safe='/&=:;#?+*')
            elif '@' in middle and not ':' in middle and simple_email_re.match(middle):
                url = 'mailto:%s' % middle
                nofollow_attr = ''
            # Make link.
            if url:
                words[i] = mark_safe('%s<%s>%s' % (lead, url, trail))
            else:
                if safe_input:
                    words[i] = mark_safe(word)
        elif safe_input:
            words[i] = mark_safe(word)
    return u''.join(words)

linebreak_re = re.compile(r'(\n|\r)')

@register.filter
def remove_linebreaks(s):
    return linebreak_re.sub(' ', s)

p_re = re.compile(r'(<p>|</p>|<br( /)?>)')

@register.filter
def remove_p(s):
    return p_re.sub('', s) 

remove_p.is_safe = True

