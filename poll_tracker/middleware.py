from django.http import HttpResponsePermanentRedirect


class HttpsToHttpMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.is_secure():
            url = request.build_absolute_uri()
            url = url.replace('https://', 'http://', 1)
            return HttpResponsePermanentRedirect(url)
        response = self.get_response(request)
        return response
