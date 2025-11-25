# fronend/admin.py
from django.contrib import admin
from .models import Banner, Mahsulot, Sevimli, Category

@admin.register(Banner)
class BannerAdmin(admin.ModelAdmin):
    list_display = ['title', 'device_type', 'is_active', 'created_at']
    list_filter = ['device_type', 'is_active', 'created_at']
    search_fields = ['title']
    list_editable = ['is_active']
    
    fieldsets = (
        ('Asosiy maʼlumotlar', {
            'fields': ('title', 'image', 'device_type', 'link', 'is_active')
        }),
    )
    
    def get_queryset(self, request):
        return super().get_queryset(request).order_by('-created_at')

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
    
    def narx_formatted(self, obj):
        return obj.narx_formatted()
    narx_formatted.short_description = 'Narx'
    
    def sotilgan_ha_yoq(self, obj):
        return obj.sotilgan_ha_yoq()
    sotilgan_ha_yoq.short_description = 'Holati'

@admin.register(Sevimli)
class SevimliAdmin(admin.ModelAdmin):
    list_display = ['user', 'mahsulot', 'sana']
    list_filter = ['sana']
    search_fields = ['user__username', 'mahsulot__name']