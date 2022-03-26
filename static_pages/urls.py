from django.urls import path

import static_pages.views

urlpatterns = [
    path('<slug:slug>/', static_pages.views.ShowPage.as_view(), name='static_page'),
]
