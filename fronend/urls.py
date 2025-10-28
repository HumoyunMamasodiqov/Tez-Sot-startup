from django.urls import path
from . import views

urlpatterns = [
    path('', views.home_view, name='home'),
    path('', views.index, name='mahsulotlar'),
    path('qosjso/', views.qosjso_view, name='qosjso'),
    path('test404/', views.test_404, name='test_404'),
    path('profil/', views.profil_view, name='profil'),
    path('elon-qoshish/', views.elon_qoshish_view, name='elon_qoshish'),
      path('mening-elonlarim/', views.mening_elonlarim_view, name='mening_elonlarim'),
    path('sotilgan-qilish/<int:mahsulot_id>/', views.sotilgan_qilish_view, name='sotilgan_qilish'),
    path('elon-ochirish/<int:mahsulot_id>/', views.elon_ochirish_view, name='elon_ochirish'),

    path('sevimliga-qoshish/<int:mahsulot_id>/', views.sevimliga_qoshish_view, name='sevimliga_qoshish'),
    path('sevimlilarim/', views.sevimlilarim_view, name='sevimlilarim'),
    path('sevimlidan-ochirish/<int:sevimli_id>/', views.sevimlidan_ochirish_view, name='sevimlidan_ochirish')
]