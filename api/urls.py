from django.urls import path

from .views import PhotoList

urlpatterns = [
    path('photos/', PhotoList.as_view()),
]
