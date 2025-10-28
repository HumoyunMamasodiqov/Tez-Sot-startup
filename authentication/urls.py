from django.urls import path
from . import views

urlpatterns = [
    
    path('kirish/', views.kirish_view, name='kirish'),
    path('chiqish/', views.chiqish_view, name='chiqish'),
    path('signup/', views.signup_view, name='signup'),
]