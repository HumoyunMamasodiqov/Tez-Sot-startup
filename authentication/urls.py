# authentication/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.kirish_view, name='login'),  # login nomi bilan
    path('signup/', views.signup_view, name='signup'),  # signup nomi bilan
    path('logout/', views.chiqish_view, name='logout'),
    path('', views.home_view, name='home'),
]