# fronend/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponseNotFound
from django.utils import timezone
from django.core.paginator import Paginator
from .models import Mahsulot, Sevimli
import re

def test_404(request):
    """404 sahifasini ko'rsatish"""
    return HttpResponseNotFound(render(request, '404.html'))

def home_view(request):
    """Bosh sahifa - oxirgi 8 ta mahsulot"""
    try:
        mahsulotlar = Mahsulot.objects.all().order_by('-id')[:8]
        return render(request, 'home.html', {'mahsulotlar': mahsulotlar})
    except Exception as e:
        print(f"DEBUG: Xatolik - {e}")
        return render(request, 'home.html', {'mahsulotlar': []})

def index(request):
    """Barcha mahsulotlar sahifasi"""
    try:
        mahsulotlar = Mahsulot.objects.all().order_by('-id')
        return render(request, 'index.html', {'mahsulotlar': mahsulotlar})
    except Exception as e:
        print(f"DEBUG: Xatolik - {e}")
        return render(request, 'index.html', {'mahsulotlar': []})

def qosjso_view(request):
    """Qo'shimcha sahifa"""
    return render(request, 'qosjso.html')

def profil_view(request):
    """Profil sahifasi"""
    return render(request, 'profil.html')

def bizhaqimizda_view(request):
    """Biz haqimizda sahifasi"""
    return render(request, 'bizhaqimizda.html')

def boglanish_view(request):
    """Bog'lanish sahifasi"""
    return render(request, 'boglanish.html')

@login_required
def elon_qoshish_view(request):
    """Yangi e'lon qo'shish"""
    if request.method == 'POST':
        try:
            # Asosiy maydonlar
            category = request.POST.get('category')
            mahsulotturi = request.POST.get('mahsulotturi')
            name = request.POST.get('name')
            viloyat = request.POST.get('viloyat')
            tuman = request.POST.get('tuman', '')
            manzil = request.POST.get('manzil', '')
            telefon = request.POST.get('telefon', '')
            telegram_username = request.POST.get('telegram_username', '')
            email = request.POST.get('email', '')
            tavsif = request.POST.get('tavsif', '')
            
            narx_input = request.POST.get('narx', '0')
            
            # Fayllar
            asosiyimg = request.FILES.get('asosiyimg')
            birimg = request.FILES.get('birimg')
            ikkiimg = request.FILES.get('ikkiimg')
            uchuimg = request.FILES.get('uchuimg')
            toltirish = request.FILES.get('toltirish')

            # Majburiy maydonlarni tekshirish
            if not all([category, mahsulotturi, name, viloyat, narx_input, asosiyimg]):
                messages.error(request, "Iltimos, barcha majburiy maydonlarni to'ldiring")
                return render(request, 'elon_qoshish.html')

            # Narxni tozalash
            cleaned_narx = ''.join(c for c in narx_input if c.isdigit() or c in '.,')
            if not cleaned_narx:
                cleaned_narx = "0"

            # Telefon raqamini tozalash
            if telefon:
                telefon = re.sub(r'\D', '', telefon)

            # Telegram username ni tozalash
            if telegram_username:
                telegram_username = telegram_username.lstrip('@')

            mahsulot = Mahsulot(
                user=request.user,
                category=category,
                mahsulotturi=mahsulotturi,
                name=name,
                viloyat=viloyat,
                tuman=tuman,
                manzil=manzil,
                telefon=telefon,
                telegram_username=telegram_username,
                email=email,
                tavsif=tavsif,
                narx=cleaned_narx,
                asosiyimg=asosiyimg,
                birimg=birimg,
                ikkiimg=ikkiimg,
                uchuimg=uchuimg,
                toltirish=toltirish,
                sana=timezone.now(),
                sotilgan=False,
                aktiv=True
            )
            
            mahsulot.save()
            
            messages.success(request, f'"{name}" mahsuloti muvaffaqiyatli qo\'shildi!')
            return redirect('mahsulot_detail', mahsulot_id=mahsulot.id)
            
        except Exception as e:
            messages.error(request, f'Xatolik yuz berdi: {str(e)}')
    
    return render(request, 'elon_qoshish.html')

@login_required
def mening_elonlarim_view(request):
    """Foydalanuvchining o'z e'lonlari"""
    try:
        status = request.GET.get('status')
        mahsulotlar = Mahsulot.objects.filter(user=request.user).order_by('-id')
        
        if status == 'yangi':
            mahsulotlar = mahsulotlar.filter(sotilgan=False)
        elif status == 'sotilgan':
            mahsulotlar = mahsulotlar.filter(sotilgan=True)
        
        paginator = Paginator(mahsulotlar, 12)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        
        return render(request, 'mening_elonlarim.html', {
            'mahsulotlar': page_obj,
            'page_obj': page_obj
        })
    except Exception as e:
        print(f"DEBUG: Xatolik - {e}")
        return render(request, 'mening_elonlarim.html', {'mahsulotlar': []})

@login_required
def sotilgan_qilish_view(request, mahsulot_id):
    """Mahsulotni sotilgan qilish"""
    mahsulot = get_object_or_404(Mahsulot, id=mahsulot_id, user=request.user)
    mahsulot.sotilgan = True
    mahsulot.save()
    messages.success(request, f'"{mahsulot.name}" sotilganlar ro\'yxatiga o\'tkazildi!')
    return redirect('mening_elonlarim')

@login_required
def elon_ochirish_view(request, mahsulot_id):
    """E'lonni o'chirish"""
    mahsulot = get_object_or_404(Mahsulot, id=mahsulot_id, user=request.user)
    mahsulot_name = mahsulot.name
    mahsulot.delete()
    messages.success(request, f'"{mahsulot_name}" e\'loni o\'chirildi!')
    return redirect('mening_elonlarim')

@login_required
def sevimliga_qoshish_view(request, mahsulot_id):
    """Mahsulotni sevimlilarga qo'shish"""
    try:
        mahsulot = get_object_or_404(Mahsulot, id=mahsulot_id)
        
        sevimli, created = Sevimli.objects.get_or_create(
            user=request.user,
            mahsulot=mahsulot
        )
        
        if created:
            messages.success(request, f'"{mahsulot.name}" sevimlilarga qo\'shildi! ❤️')
        else:
            messages.info(request, f'"{mahsulot.name}" allaqachon sevimlilaringizda bor')
            
        return redirect(request.META.get('HTTP_REFERER', 'home'))
        
    except Exception as e:
        messages.error(request, f'Xatolik yuz berdi: {str(e)}')
        return redirect('home')

@login_required
def sevimlilarim_view(request):
    """Foydalanuvchining sevimli mahsulotlari"""
    try:
        sevimlilar = Sevimli.objects.filter(user=request.user).order_by('-sana')
        return render(request, 'sevimlilar.html', {'sevimlilar': sevimlilar})
    except Exception as e:
        print(f"DEBUG: Xatolik - {e}")
        return render(request, 'sevimlilar.html', {'sevimlilar': []})

@login_required
def sevimlidan_ochirish_view(request, sevimli_id):
    """Mahsulotni sevimlilardan olib tashlash"""
    try:
        sevimli = get_object_or_404(Sevimli, id=sevimli_id, user=request.user)
        mahsulot_nomi = sevimli.mahsulot.name
        sevimli.delete()
        messages.success(request, f'"{mahsulot_nomi}" sevimlilardan olib tashlandi')
        return redirect('sevimlilarim')
    except Exception as e:
        messages.error(request, f'Xatolik yuz berdi: {str(e)}')
        return redirect('sevimlilarim')

def mahsulot_detail_view(request, mahsulot_id):
    """Mahsulot tafsilotlari sahifasi"""
    try:
        mahsulot = get_object_or_404(Mahsulot, id=mahsulot_id)
        
        # Ko'rishlar sonini oshirish
        mahsulot.korishlar_soni += 1
        mahsulot.save(update_fields=['korishlar_soni'])
        
        # O'xshash mahsulotlarni olish (bir xil kategoriyadagi)
        o_xshash_mahsulotlar = Mahsulot.objects.filter(
            category=mahsulot.category,
            aktiv=True
        ).exclude(id=mahsulot_id).order_by('-id')[:4]
        
        return render(request, 'mahsulot_detail.html', {
            'mahsulot': mahsulot,
            'o_xshash_mahsulotlar': o_xshash_mahsulotlar
        })
    except Exception as e:
        messages.error(request, f'Mahsulot topilmadi: {str(e)}')
        return redirect('mahsulotlar')