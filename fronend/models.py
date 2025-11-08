# fronend/models.py
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
import re

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
    tuman = models.CharField(max_length=100, verbose_name="Tuman/Shahar", blank=True, null=True)
    manzil = models.TextField(verbose_name="Aniq manzil", blank=True, null=True)
    telefon = models.CharField(max_length=20, verbose_name="Telefon raqam", blank=True, null=True)
    telegram_username = models.CharField(max_length=100, verbose_name="Telegram username", blank=True, null=True)
    email = models.EmailField(verbose_name="Email", blank=True, null=True)
    tavsif = models.TextField(verbose_name="Batafsil tavsif", blank=True, null=True)
    
    sana = models.DateField(default=timezone.now, verbose_name="Sana")
    narx = models.CharField(max_length=20, verbose_name="Narx", default="0")
    
    asosiyimg = models.ImageField(upload_to='asosiyimg/', verbose_name="Asosiy rasm")
    birimg = models.ImageField(upload_to='birimg/', verbose_name="1-rasm", blank=True, null=True)
    ikkiimg = models.ImageField(upload_to='ikkiimg/', verbose_name="2-rasm", blank=True, null=True)
    uchuimg = models.ImageField(upload_to='uchuimg/', verbose_name="3-rasm", blank=True, null=True)
    toltirish = models.FileField(upload_to='toltirish/', verbose_name="Qo'shimcha fayl", blank=True, null=True)
    
    sotilgan = models.BooleanField(default=False, verbose_name="Sotildi")
    aktiv = models.BooleanField(default=True, verbose_name="Aktiv")
    korishlar_soni = models.PositiveIntegerField(default=0, verbose_name="Ko'rishlar soni")

    class Meta:
        verbose_name = "Mahsulot"
        verbose_name_plural = "Mahsulotlar"
        ordering = ['-sana']

    def __str__(self):
        return f"{self.name} - {self.user.username}"

    def narx_formatted(self):
        """Narxni formatlash"""
        try:
            if not self.narx:
                return "0 so'm"
            
            narx_str = str(self.narx).replace(',', '.').strip()
            if narx_str and narx_str != '.':
                narx_str = re.sub(r'[^\d.]', '', narx_str)
                if narx_str and narx_str != '.':
                    narx_float = float(narx_str)
                    if narx_float.is_integer():
                        return f"{int(narx_float):,} so'm".replace(',', ' ')
                    else:
                        return f"{narx_float:,.2f} so'm".replace(',', ' ').replace('.', ',')
            return "0 so'm"
                
        except (ValueError, TypeError, AttributeError):
            return "0 so'm"
    
    narx_formatted.short_description = 'Narx'

    def user_info(self):
        """Foydalanuvchi ma'lumotlari"""
        if self.user.first_name and self.user.last_name:
            return f"{self.user.first_name} {self.user.last_name}"
        return self.user.username
    
    user_info.short_description = 'Foydalanuvchi'

    def telefon_formatted(self):
        """Telefon raqamini formatlash"""
        if not self.telefon:
            return "Ko'rsatilmagan"
        
        numbers = re.sub(r'\D', '', self.telefon)
        if len(numbers) == 9:
            return f"+998 {numbers[:2]} {numbers[2:5]} {numbers[5:7]} {numbers[7:]}"
        elif len(numbers) == 12 and numbers.startswith('998'):
            return f"+{numbers[:3]} {numbers[3:5]} {numbers[5:8]} {numbers[8:10]} {numbers[10:]}"
        else:
            return self.telefon

    def toliq_manzil(self):
        """To'liq manzilni qaytarish"""
        manzil_qismlari = []
        if self.viloyat:
            manzil_qismlari.append(self.get_viloyat_display())
        if self.tuman:
            manzil_qismlari.append(self.tuman)
        if self.manzil:
            manzil_qismlari.append(self.manzil)
        
        return ", ".join(manzil_qismlari) if manzil_qismlari else "Manzil ko'rsatilmagan"

    def telegram_link(self):
        """Telegram linkini yaratish"""
        if self.telegram_username:
            username = self.telegram_username.lstrip('@')
            return f"https://t.me/{username}"
        return "#"

    def telefon_link(self):
        """Telefon linkini yaratish"""
        if self.telefon:
            numbers = re.sub(r'\D', '', self.telefon)
            if numbers:
                return f"tel:+998{numbers[-9:]}" if len(numbers) >= 9 else f"tel:{numbers}"
        return "#"

    def sotilgan_ha_yoq(self):
        """Sotilgan holatini ko'rsatish"""
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


class Category(models.Model):
    name = models.CharField(max_length=100, verbose_name="Kategoriya nomi")
    description = models.TextField(blank=True, verbose_name="Tavsif")
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = "Kategoriya"
        verbose_name_plural = "Kategoriyalar"
        ordering = ['name']
    
    def __str__(self):
        return self.name