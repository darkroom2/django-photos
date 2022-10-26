from django.urls import path

from .views import PhotoListCreate

urlpatterns = [
    path('photos/', PhotoListCreate.as_view()),
]
