import pytest
from django.test import Client
from django.urls import reverse


class TestViews:
    @pytest.mark.django_db
    def test_login_success(self, user):
        client = Client()
        data = {
            'username': 'test',
            'password': '123456',
        }
        response = client.post(reverse('login'), data)
        assert response.status_code == 302
        assert response.url.startswith(reverse('index'))

    @pytest.mark.django_db
    def test_login_error(self):
        client = Client()
        data = {
            'username': 'test',
            'password': '123456',
        }
        response = client.post(reverse('login'), data)
        assert response.status_code == 200

    @pytest.mark.django_db
    def test_register_success(self, user):
        client = Client()
        data = {
            'email': 'test2@test.pl',
            'password': '123456',
            'first_name': 'first_name',
            'last_name': 'last_name',
        }
        response = client.post(reverse('register'), data)
        assert response.status_code == 302
        assert response.url.startswith(reverse('index'))

    @pytest.mark.django_db
    def test_register_error(self, user):
        client = Client()
        data = {
            'email': '',
            'password': '',
        }
        response = client.post(reverse('register'), data)
        assert response.status_code == 200
