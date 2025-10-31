from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    
    path('kirish/', views.kirish_view, name='kirish'),
    path('chiqish/', views.chiqish_view, name='chiqish'),
    path('signup/', views.signup_view, name='signup'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)