from django.http import Http404


class CurrentOrgMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        from .models import Organization

        try:
            request.org = Organization.objects.get_current(request)
        except Organization.DoesNotExist:
            raise Http404("Organization does not exist")
        return self.get_response(request)