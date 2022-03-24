from django.views.generic import TemplateView, DetailView
from django.shortcuts import get_object_or_404

from static_page.models import StaticPage


class ShowPage(DetailView):
    model = StaticPage
    template_name = 'static_page/static_page.html'

    def get_object(self, queryset=None):
        return get_object_or_404(StaticPage, slug=self.kwargs.get('slug'))


class Index(TemplateView):
    template_name = 'static_page/index.html'
