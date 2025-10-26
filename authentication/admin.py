# admin.py
from django.contrib import admin
from .models import Profile

class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'birth_date', 'phone', )
    search_fields = ('user__username', 'user__email', 'user__first_name', 'user__last_name', 'phone')
    list_filter = ('birth_date',)
    
    # Barcha maydonlarni ko'rsatish
    fields = ('user', 'birth_date', 'phone',)

admin.site.register(Profile, ProfileAdmin)