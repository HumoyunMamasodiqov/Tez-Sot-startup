# frontend/urls.py
from django.urls import path
from . import views


urlpatterns = [
    path('', views.home_view, name='home'),
    path('qosjso/', views.qosjso_view, name='qosjso'),
    path('test404/', views.test_404),
]
