import pytest
from django.test import Client
from django.urls import reverse


class TestViews:
    @pytest.mark.django_db
    def test_index(self):
        client = Client()
        assert client.get(reverse('index')).status_code == 200

    @pytest.mark.django_db
    def test_static_page_detail_valid(self, static_pages):
        client = Client()
        for static_page in static_pages:
            response = client.get(reverse('static_page', args=(static_page.slug,)))
            assert response.status_code == 200
            assert response.context['object'].body == static_page.body

    @pytest.mark.django_db
    def test_static_page_detail_not_found(self):
        client = Client()
        response = client.get(reverse('static_page', args=('not-valid',)))
        assert response.status_code == 404
