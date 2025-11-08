# fronend/urls.py
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    path('', views.home_view, name='home'),
    path('mahsulotlar/', views.index, name='mahsulotlar'),
    path('barcha-mahsulotlar/', views.barcha_mahsulotlar, name='barcha_mahsulotlar'),
    path('qosjso/', views.qosjso_view, name='qosjso'),
    path('test404/', views.test_404, name='test_404'),
    path('profil/', views.profil_view, name='profil'),
    path('boglanish/', views.boglanish_view, name='boglanish'),
    path('bizhaqimizda/', views.bizhaqimizda_view, name='biz_haqimizda'),
    path('elon-qoshish/', views.elon_qoshish_view, name='elon_qoshish'),
    path('mening-elonlarim/', views.mening_elonlarim_view, name='mening_elonlarim'),
    path('sotilgan-qilish/<int:mahsulot_id>/', views.sotilgan_qilish_view, name='sotilgan_qilish'),
    path('elon-ochirish/<int:mahsulot_id>/', views.elon_ochirish_view, name='elon_ochirish'),
    path('mahsulot/<int:mahsulot_id>/', views.mahsulot_detail_view, name='mahsulot_detail'),
    path('sevimliga-qoshish/<int:mahsulot_id>/', views.sevimliga_qoshish_view, name='sevimliga_qoshish'),
    path('sevimlilarim/', views.sevimlilarim_view, name='sevimlilarim'),
    path('sevimlidan-ochirish/<int:sevimli_id>/', views.sevimlidan_ochirish_view, name='sevimlidan_ochirish'),
    path('api/search/', views.api_search, name='api_search'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)