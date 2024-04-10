from django.urls import path

from .views import RateAPI

urlpatterns = [
    path("rates/", RateAPI.as_view()),
]
