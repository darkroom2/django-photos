from django.urls import path

from .views import PhotoListCreate, PhotoRetrieveUpdateDestroy, PhotosUploadListCreate

urlpatterns = [
    path('photos/', PhotoListCreate.as_view()),
    path('photos/<int:pk>', PhotoRetrieveUpdateDestroy.as_view()),
    path('photos_load/', PhotosUploadListCreate.as_view()),
]
