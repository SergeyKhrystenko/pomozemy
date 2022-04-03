import pytest
from django.contrib.auth.models import User
from datetime import datetime, timedelta

from django.utils.timezone import make_aware

from fundraisers.models import Fundraiser, Category


@pytest.fixture
def users():
    lst = []
    for i in range(10):
        lst.append(
            User.objects.create_user(username=f'test{i}', password='123456')
        )
    return lst


@pytest.fixture
def categories():
    lst = []
    for i in range(10):
        lst.append(
            Category.objects.create(
                name=f'Test {i}',
            )
        )
    return lst


@pytest.fixture
def fundraisers(users, categories):
    lst = []
    for i in range(10):
        lst.append(
            Fundraiser.objects.create(
                name=i,
                description=f'Test description {i}',
                owner=users[i],
                purpose=100,
                active=True,
                start_date=make_aware(datetime.now()),
                end_date=make_aware(datetime.now() + timedelta(days=30)),
                category=categories[i],
            )
        )
    return lst
