from django.urls import path

from .views import PhotoListCreate, PhotoRetrieveUpdateDestroy, PhotosUploadCreate

urlpatterns = [
    path('photos/', PhotoListCreate.as_view()),
    path('photos/<int:pk>', PhotoRetrieveUpdateDestroy.as_view()),
    path('photos/import/', PhotosUploadCreate.as_view()),
]
