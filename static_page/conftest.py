import pytest

from static_page.models import StaticPage


@pytest.fixture
def static_pages():
    lst = []
    for i in range(10):
        lst.append(
            StaticPage.objects.create(title=i, body=f'Page #{i}')
        )
    return lst
