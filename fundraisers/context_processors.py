from fundraisers.models import Category


def fundraisers_context(request):
    return {
        'categories': Category.objects.all(),
    }
