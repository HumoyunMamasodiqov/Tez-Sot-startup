# fronend/admin.py
from django.contrib import admin
from .models import Mahsulot, Sevimli

@admin.register(Mahsulot)
class MahsulotAdmin(admin.ModelAdmin):
    list_display = ['name', 'user_info', 'category', 'viloyat', 'narx_formatted', 'sotilgan_ha_yoq', 'sana']
    list_filter = ['category', 'viloyat', 'sotilgan', 'sana']
    search_fields = ['name', 'mahsulotturi', 'user__username']
    readonly_fields = ['sana']
    
    def get_queryset(self, request):
        return super().get_queryset(request)

@admin.register(Sevimli)
class SevimliAdmin(admin.ModelAdmin):
    list_display = ['user', 'mahsulot', 'sana']
    list_filter = ['sana']
    search_fields = ['user__username', 'mahsulot__name']
    readonly_fields = ['sana']