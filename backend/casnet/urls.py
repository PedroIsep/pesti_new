from django.urls import path
from .views import process_image, process_video

urlpatterns = [
    path('process-image/', process_image, name='process_image'),
    path('process-video/', process_video, name='process_video'),
]
