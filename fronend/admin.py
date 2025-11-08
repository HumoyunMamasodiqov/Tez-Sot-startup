# fronend/admin.py
from django.contrib import admin
from .models import Mahsulot, Sevimli, Category

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'created_at']
    search_fields = ['name']
    list_filter = ['created_at']

@admin.register(Mahsulot)
class MahsulotAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'narx_formatted', 'viloyat', 'sana', 'sotilgan_ha_yoq', 'aktiv']
    list_filter = ['category', 'viloyat', 'sotilgan', 'aktiv', 'sana']
    search_fields = ['name', 'tavsif', 'category', 'mahsulotturi']
    date_hierarchy = 'sana'
    readonly_fields = ['korishlar_soni']

@admin.register(Sevimli)
class SevimliAdmin(admin.ModelAdmin):
    list_display = ['user', 'mahsulot', 'sana']
    list_filter = ['sana']
    search_fields = ['user__username', 'mahsulot__name']