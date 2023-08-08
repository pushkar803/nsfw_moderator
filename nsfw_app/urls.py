from django.urls import path
from . import views

urlpatterns = [
    path('upload/', views.upload_and_classify_nsfw,
         name='upload_and_classify_nsfw'),
]
