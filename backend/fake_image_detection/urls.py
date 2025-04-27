from django.urls import path
from .views import ImageUploadView

urlpatterns = [
    path('image/upload/', ImageUploadView.as_view(), name='upload-image')
]
