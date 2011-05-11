from boar.archive.models import Volume, Issue
from django import template
from django.shortcuts import render_to_response, get_object_or_404


def issue(request, volume_slug, issue_slug):
    issue = get_object_or_404(Issue, volume__slug=volume_slug, slug=issue_slug)
    parts = []
    for part in issue.parts.all():
        spreads = [{'pages': [], 'content': []}]
        for page in part.pages.all():
            # Odd pages, append to existing spread
            if page.number & 1 == 1:
                spreads[-1]['pages'].append(page)
                spreads[-1]['content'] += list(page.articles.all())
            # Even pages, create new spread
            else:
                spreads.append({
                    'pages': [page],
                    'content': list(page.articles.all())
                })
        parts.append({'part': part, 'spreads': spreads})
    return render_to_response('archive/issue_detail.html', {
        'issue': issue,
        'parts': parts,
    }, context_instance=template.RequestContext(request))
