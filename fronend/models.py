# fronend/models.py
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

class Mahsulot(models.Model):
    CATEGORY_CHOICES = [
        ('elektronika', 'Elektronika'),
        ('uy_jihozlari', 'Uy jihozlari'),
        ('kiyim', 'Kiyim-kechak'),
        ('avto', 'Avto ehtiyot qismlar'),
        ('boshqa', 'Boshqa'),
    ]

    VILOYAT_CHOICES = [
        ('toshkent', 'Toshkent'),
        ('samarqand', 'Samarqand'),
        ('fargona', 'Farg‘ona'),
        ('andijon', 'Andijon'),
        ('namangan', 'Namangan'),
        ('buxoro', 'Buxoro'),
        ('navoiy', 'Navoiy'),
        ('xorazm', 'Xorazm'),
        ('qashqadaryo', 'Qashqadaryo'),
        ('surxondaryo', 'Surxondaryo'),
        ('jizzax', 'Jizzax'),
        ('sirdaryo', 'Sirdaryo'),
        ('qoraqalpogiston', 'Qoraqalpog‘iston'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Foydalanuvchi")
    category = models.CharField(max_length=100, choices=CATEGORY_CHOICES, verbose_name="Kategoriya")
    mahsulotturi = models.CharField(max_length=100, verbose_name="Mahsulot turi")
    name = models.CharField(max_length=100, verbose_name="Mahsulot nomi")
    viloyat = models.CharField(max_length=100, choices=VILOYAT_CHOICES, verbose_name="Viloyat")
    sana = models.DateField(default=timezone.now, verbose_name="Sana")
    
    # VAQTINCHA: CharField ga o'zgartiramiz
    narx = models.CharField(max_length=20, verbose_name="Narx", default="0")

    asosiyimg = models.ImageField(upload_to='asosiyimg/', verbose_name="Asosiy rasm")
    birimg = models.ImageField(upload_to='birimg/', verbose_name="1-rasm", blank=True, null=True)
    ikkiimg = models.ImageField(upload_to='ikkiimg/', verbose_name="2-rasm", blank=True, null=True)
    uchuimg = models.ImageField(upload_to='uchuimg/', verbose_name="3-rasm", blank=True, null=True)
    toltirish = models.FileField(upload_to='toltirish/', verbose_name="Qo'shimcha fayl", blank=True, null=True)
    sotilgan = models.BooleanField(default=False, verbose_name="Sotildi")

    class Meta:
        verbose_name = "Mahsulot"
        verbose_name_plural = "Mahsulotlar"

    def __str__(self):
        return f"{self.name} - {self.user.username}"

    def narx_formatted(self):
        """Narxni formatlash"""
        try:
            if not self.narx:
                return "0 so'm"
            
            # CharField dan raqamga o'tkazish
            narx_str = str(self.narx).replace(',', '.').strip()
            if narx_str and narx_str != '.':
                # Float ga o'tkazib formatlash
                narx_float = float(narx_str)
                if narx_float.is_integer():
                    return f"{int(narx_float):,} so'm".replace(',', ' ')
                else:
                    return f"{narx_float:,.2f} so'm".replace(',', ' ').replace('.', ',')
            else:
                return "0 so'm"
                
        except (ValueError, TypeError, AttributeError):
            return "0 so'm"
    
    narx_formatted.short_description = 'Narx'

    def user_info(self):
        if self.user.first_name and self.user.last_name:
            return f"{self.user.first_name} {self.user.last_name} ({self.user.username})"
        return self.user.username
    user_info.short_description = 'Foydalanuvchi'

    def sotilgan_ha_yoq(self):
        if self.sotilgan:
            return "✅ Sotilgan"
        return "🆕 Yangi"
    sotilgan_ha_yoq.short_description = 'Holati'


class Sevimli(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Foydalanuvchi")
    mahsulot = models.ForeignKey(Mahsulot, on_delete=models.CASCADE, verbose_name="Mahsulot")
    sana = models.DateTimeField(auto_now_add=True, verbose_name="Saqlangan sana")

    class Meta:
        verbose_name = "Sevimli"
        verbose_name_plural = "Sevimlilar"
        unique_together = ['user', 'mahsulot']

    def __str__(self):
        return f"{self.user.username} - {self.mahsulot.name}"