# frontend/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponseNotFound
from django.utils import timezone
from django.core.paginator import Paginator
from .models import Mahsulot, Sevimli
import re


def test_404(request):
    """404 sahifasini ko‘rsatish"""
    return HttpResponseNotFound(render(request, '404.html'))


def home_view(request):
    """Bosh sahifa - oxirgi 8 ta mahsulot"""
    try:
        mahsulotlar = Mahsulot.objects.filter(aktiv=True).order_by('-id')[:8]
        return render(request, 'home.html', {'mahsulotlar': mahsulotlar})
    except Exception as e:
        print(f"DEBUG: Xatolik - {e}")
        return render(request, 'home.html', {'mahsulotlar': []})


def index(request):
    """Barcha mahsulotlar sahifasi"""
    try:
        mahsulotlar = Mahsulot.objects.filter(aktiv=True).order_by('-id')
        paginator = Paginator(mahsulotlar, 12)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        return render(request, 'index.html', {'mahsulotlar': page_obj, 'page_obj': page_obj})
    except Exception as e:
        print(f"DEBUG: Xatolik - {e}")
        return render(request, 'index.html', {'mahsulotlar': []})


def qosjso_view(request):
    return render(request, 'qosjso.html')


def profil_view(request):
    return render(request, 'profil.html')


def bizhaqimizda_view(request):
    return render(request, 'bizhaqimizda.html')


def boglanish_view(request):
    return render(request, 'boglanish.html')


@login_required
def elon_qoshish_view(request):
    """Yangi e‘lon qo‘shish"""
    if request.method == 'POST':
        try:
            category = request.POST.get('category')
            mahsulotturi = request.POST.get('mahsulotturi')
            name = request.POST.get('name')
            viloyat = request.POST.get('viloyat')
            narx_input = request.POST.get('narx', '0')
            asosiyimg = request.FILES.get('asosiyimg')

            if not all([category, mahsulotturi, name, viloyat, narx_input, asosiyimg]):
                messages.error(request, "Iltimos, barcha majburiy maydonlarni to‘ldiring.")
                return render(request, 'elon_qoshish.html')

            cleaned_narx = ''.join(c for c in narx_input if c.isdigit() or c in '.,') or '0'
            telefon = re.sub(r'\D', '', request.POST.get('telefon', ''))
            telegram_username = request.POST.get('telegram_username', '').lstrip('@')

            mahsulot = Mahsulot.objects.create(
                user=request.user,
                category=category,
                mahsulotturi=mahsulotturi,
                name=name,
                viloyat=viloyat,
                tuman=request.POST.get('tuman', ''),
                manzil=request.POST.get('manzil', ''),
                telefon=telefon,
                telegram_username=telegram_username,
                email=request.POST.get('email', ''),
                tavsif=request.POST.get('tavsif', ''),
                narx=cleaned_narx,
                asosiyimg=asosiyimg,
                birimg=request.FILES.get('birimg'),
                ikkiimg=request.FILES.get('ikkiimg'),
                uchuimg=request.FILES.get('uchuimg'),
                toltirish=request.FILES.get('toltirish'),
                sana=timezone.now(),
                sotilgan=False,
                aktiv=True
            )

            messages.success(request, f'"{name}" mahsuloti muvaffaqiyatli qo‘shildi!')
            return redirect('mahsulot_detail', mahsulot_id=mahsulot.id)

        except Exception as e:
            messages.error(request, f'Xatolik yuz berdi: {str(e)}')

    return render(request, 'elon_qoshish.html')


@login_required
def mening_elonlarim_view(request):
    """Foydalanuvchining o‘z e‘lonlari"""
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

        return render(request, 'mening_elonlarim.html', {'mahsulotlar': page_obj, 'page_obj': page_obj})
    except Exception as e:
        print(f"DEBUG: Xatolik - {e}")
        return render(request, 'mening_elonlarim.html', {'mahsulotlar': []})


@login_required
def sotilgan_qilish_view(request, mahsulot_id):
    mahsulot = get_object_or_404(Mahsulot, id=mahsulot_id, user=request.user)
    mahsulot.sotilgan = True
    mahsulot.save(update_fields=['sotilgan'])
    messages.success(request, f'"{mahsulot.name}" sotilganlar ro‘yxatiga o‘tkazildi!')
    return redirect('mening_elonlarim')


@login_required
def elon_ochirish_view(request, mahsulot_id):
    mahsulot = get_object_or_404(Mahsulot, id=mahsulot_id, user=request.user)
    nom = mahsulot.name
    mahsulot.delete()
    messages.success(request, f'"{nom}" e‘loni o‘chirildi!')
    return redirect('mening_elonlarim')


@login_required
def sevimliga_qoshish_view(request, mahsulot_id):
    """Mahsulotni sevimlilarga qo‘shish"""
    try:
        mahsulot = get_object_or_404(Mahsulot, id=mahsulot_id)
        sevimli, created = Sevimli.objects.get_or_create(user=request.user, mahsulot=mahsulot)

        if created:
            messages.success(request, f'"{mahsulot.name}" sevimlilarga qo‘shildi ❤️')
        else:
            messages.info(request, f'"{mahsulot.name}" allaqachon sevimlilarda bor.')

        return redirect(request.META.get('HTTP_REFERER', 'home'))

    except Exception as e:
        messages.error(request, f'Xatolik yuz berdi: {str(e)}')
        return redirect('home')


@login_required
def sevimlilarim_view(request):
    """Foydalanuvchining sevimlilari"""
    try:
        sevimlilar = Sevimli.objects.filter(user=request.user).order_by('-sana')
        return render(request, 'sevimlilar.html', {'sevimlilar': sevimlilar})
    except Exception as e:
        print(f"DEBUG: Xatolik - {e}")
        return render(request, 'sevimlilar.html', {'sevimlilar': []})


@login_required
def sevimlidan_ochirish_view(request, sevimli_id):
    """Sevimlilardan olib tashlash"""
    try:
        sevimli = get_object_or_404(Sevimli, id=sevimli_id, user=request.user)
        nom = sevimli.mahsulot.name
        sevimli.delete()
        messages.success(request, f'"{nom}" sevimlilardan olib tashlandi.')
        return redirect('sevimlilarim')
    except Exception as e:
        messages.error(request, f'Xatolik yuz berdi: {str(e)}')
        return redirect('sevimlilarim')


def mahsulot_detail_view(request, mahsulot_id):
    """Mahsulot tafsilotlari (login bo‘lmaganlar ham kiradi)"""
    try:
        mahsulot = get_object_or_404(Mahsulot, id=mahsulot_id)

        if request.user.is_authenticated:
            mahsulot.korishlar_soni += 1
            mahsulot.save(update_fields=['korishlar_soni'])

        o_xshash = Mahsulot.objects.filter(
            category=mahsulot.category,
            aktiv=True
        ).exclude(id=mahsulot.id).order_by('-id')[:4]

        return render(request, 'mahsulot_detail.html', {
            'mahsulot': mahsulot,
            'o_xshash_mahsulotlar': o_xshash
        })

    except Mahsulot.DoesNotExist:
        messages.error(request, "Mahsulot topilmadi yoki o‘chirilgan.")
        return redirect('index')
    except Exception as e:
        print(f"DEBUG: Xatolik - {e}")
        messages.error(request, "Noma’lum xatolik yuz berdi.")
        return redirect('index')
