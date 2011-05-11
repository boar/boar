from django import http

class ArticleMiddleware(object):
    def process_request(self, request):
        # Redirect archive form GET request to actual archive page
        if 'month' in request.GET and request.GET['month']:
            try:
                (year, month) = request.GET['month'].split('-')
            except ValueError:
                raise http.Http404
            return http.HttpResponsePermanentRedirect('%s%s/%s/' % (request.path, year, month))
        