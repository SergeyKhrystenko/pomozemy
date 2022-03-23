from django.views import View
from django.http import HttpRequest, HttpResponse


class ShowPage(View):
    def get(self, request: HttpRequest, slug: str) -> HttpResponse:
        return HttpResponse(slug)
