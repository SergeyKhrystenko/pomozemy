from django.urls import path

import static_page.views

urlpatterns = [
    path('<slug:slug>/', static_page.views.ShowPage.as_view()),
]
