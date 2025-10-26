# urls.py (asosiy loyiha)
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('auth/', include('authentication.urls')),  # authentication app uchun
    path('', include('fronend.urls')),  # bosh sahifa uchun
]