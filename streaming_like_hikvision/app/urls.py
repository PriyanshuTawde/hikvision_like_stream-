# app/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('', views.video_grid, name='video_grid'),
    path('health/<int:camera_number>/', views.health_check, name='health_check'),
]
