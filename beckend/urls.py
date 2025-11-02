from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.shortcuts import render
import os


# 404 sahifa
def custom_404(request, exception):
    return render(request, '404.html', status=404)

handler404 = custom_404

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('fronend.urls')),  # asosiy app
    path('auth/', include('authentication.urls')),  # auth app
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)