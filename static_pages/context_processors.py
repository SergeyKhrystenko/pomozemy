from static_pages.models import StaticPage


def static_pages_context(request):
    return {
        'static_pages': StaticPage.objects.all(),
    }
