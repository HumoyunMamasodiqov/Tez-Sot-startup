# fronend/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponseNotFound
from .models import Mahsulot
from django.utils import timezone
from django.core.paginator import Paginator
from .models import Mahsulot, Sevimli
def test_404(request):
    return HttpResponseNotFound(render(request, '404.html'))

def home_view(request):
    try:
        # BARCHA mahsulotlarni ko'rsatamiz (sotilgan va sotilmagan)
        mahsulotlar = Mahsulot.objects.all().order_by('-id')[:8]  # FILTER O'CHIRILDI
        return render(request, 'home.html', {'mahsulotlar': mahsulotlar})
    except Exception as e:
        print(f"DEBUG: Xatolik - {e}")
        return render(request, 'home.html', {'mahsulotlar': []})

def index(request):
    try:
        # BARCHA mahsulotlarni ko'rsatamiz (sotilgan va sotilmagan)
        mahsulotlar = Mahsulot.objects.all().order_by('-id')  # FILTER O'CHIRILDI
        return render(request, 'index.html', {'mahsulotlar': mahsulotlar})
    except Exception as e:
        print(f"DEBUG: Xatolik - {e}")
        return render(request, 'index.html', {'mahsulotlar': []})

def qosjso_view(request):
    return render(request, 'qosjso.html')

def profil_view(request):
    return render(request, 'profil.html')

@login_required
def elon_qoshish_view(request):
    if request.method == 'POST':
        try:
            category = request.POST.get('category')
            mahsulotturi = request.POST.get('mahsulotturi')
            name = request.POST.get('name')
            viloyat = request.POST.get('viloyat')
            narx = request.POST.get('narx')
            
            asosiyimg = request.FILES.get('asosiyimg')
            birimg = request.FILES.get('birimg')
            ikkiimg = request.FILES.get('ikkiimg')
            uchuimg = request.FILES.get('uchuimg')
            toltirish = request.FILES.get('toltirish')

            if not all([category, mahsulotturi, name, viloyat, narx, asosiyimg]):
                messages.error(request, "Iltimos, barcha majburiy maydonlarni to'ldiring")
                return render(request, 'elon_qoshish.html')

            mahsulot = Mahsulot(
                user=request.user,
                category=category,
                mahsulotturi=mahsulotturi,
                name=name,
                viloyat=viloyat,
                narx=narx,
                asosiyimg=asosiyimg,
                birimg=birimg,
                ikkiimg=ikkiimg,
                uchuimg=uchuimg,
                toltirish=toltirish,
                sana=timezone.now(),
                sotilgan=False  # Yangi qo'shilgan har doim "Yangi"
            )
            
            mahsulot.save()
            
            messages.success(request, f'"{name}" mahsuloti muvaffaqiyatli qo\'shildi!')
            return redirect('mahsulotlar')
            
        except Exception as e:
            messages.error(request, f'Xatolik yuz berdi: {str(e)}')
    
    return render(request, 'elon_qoshish.html')
             
# fronend/views.py - elon_qoshish_view funksiyasini tuzatish
# fronend/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponseNotFound
from .models import Mahsulot, Sevimli
from django.utils import timezone
from django.core.paginator import Paginator

def test_404(request):
    return HttpResponseNotFound(render(request, '404.html'))

def home_view(request):
    try:
        mahsulotlar = Mahsulot.objects.all().order_by('-id')[:8]
        return render(request, 'home.html', {'mahsulotlar': mahsulotlar})
    except Exception as e:
        print(f"DEBUG: Xatolik - {e}")
        return render(request, 'home.html', {'mahsulotlar': []})

def index(request):
    try:
        mahsulotlar = Mahsulot.objects.all().order_by('-id')
        return render(request, 'index.html', {'mahsulotlar': mahsulotlar})
    except Exception as e:
        print(f"DEBUG: Xatolik - {e}")
        return render(request, 'index.html', {'mahsulotlar': []})

def qosjso_view(request):
    return render(request, 'qosjso.html')

def profil_view(request):
    return render(request, 'profil.html')

@login_required
def elon_qoshish_view(request):
    if request.method == 'POST':
        try:
            category = request.POST.get('category')
            mahsulotturi = request.POST.get('mahsulotturi')
            name = request.POST.get('name')
            viloyat = request.POST.get('viloyat')
            narx_input = request.POST.get('narx', '0')
            
            asosiyimg = request.FILES.get('asosiyimg')
            birimg = request.FILES.get('birimg')
            ikkiimg = request.FILES.get('ikkiimg')
            uchuimg = request.FILES.get('uchuimg')
            toltirish = request.FILES.get('toltirish')

            if not all([category, mahsulotturi, name, viloyat, narx_input, asosiyimg]):
                messages.error(request, "Iltimos, barcha majburiy maydonlarni to'ldiring")
                return render(request, 'elon_qoshish.html')

            # Narxni tozalash
            cleaned_narx = ''.join(c for c in narx_input if c.isdigit() or c in '.,')
            if not cleaned_narx:
                cleaned_narx = "0"

            mahsulot = Mahsulot(
                user=request.user,
                category=category,
                mahsulotturi=mahsulotturi,
                name=name,
                viloyat=viloyat,
                narx=cleaned_narx,
                asosiyimg=asosiyimg,
                birimg=birimg,
                ikkiimg=ikkiimg,
                uchuimg=uchuimg,
                toltirish=toltirish,
                sana=timezone.now(),
                sotilgan=False
            )
            
            mahsulot.save()
            
            messages.success(request, f'"{name}" mahsuloti muvaffaqiyatli qo\'shildi!')
            return redirect('mahsulotlar')
            
        except Exception as e:
            messages.error(request, f'Xatolik yuz berdi: {str(e)}')
    
    return render(request, 'elon_qoshish.html')

@login_required
def mening_elonlarim_view(request):
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
    mahsulot = get_object_or_404(Mahsulot, id=mahsulot_id, user=request.user)
    mahsulot.sotilgan = True
    mahsulot.save()
    messages.success(request, f'"{mahsulot.name}" sotilganlar ro\'yxatiga o\'tkazildi!')
    return redirect('mening_elonlarim')

@login_required
def elon_ochirish_view(request, mahsulot_id):
    mahsulot = get_object_or_404(Mahsulot, id=mahsulot_id, user=request.user)
    mahsulot_name = mahsulot.name
    mahsulot.delete()
    messages.success(request, f'"{mahsulot_name}" e\'loni o\'chirildi!')
    return redirect('mening_elonlarim')

@login_required
def sevimliga_qoshish_view(request, mahsulot_id):
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
    try:
        sevimlilar = Sevimli.objects.filter(user=request.user).order_by('-sana')
        return render(request, 'sevimlilar.html', {'sevimlilar': sevimlilar})
    except Exception as e:
        print(f"DEBUG: Xatolik - {e}")
        return render(request, 'sevimlilar.html', {'sevimlilar': []})

@login_required
def sevimlidan_ochirish_view(request, sevimli_id):
    try:
        sevimli = get_object_or_404(Sevimli, id=sevimli_id, user=request.user)
        mahsulot_nomi = sevimli.mahsulot.name
        sevimli.delete()
        messages.success(request, f'"{mahsulot_nomi}" sevimlilardan olib tashlandi')
        return redirect('sevimlilarim')
    except Exception as e:
        messages.error(request, f'Xatolik yuz berdi: {str(e)}')
        return redirect('sevimlilarim')
@login_required
def mening_elonlarim_view(request):
    # Filtrlash
    status = request.GET.get('status')
    mahsulotlar = Mahsulot.objects.filter(user=request.user).order_by('-id')
    
    if status == 'yangi':
        mahsulotlar = mahsulotlar.filter(sotilgan=False)
    elif status == 'sotilgan':
        mahsulotlar = mahsulotlar.filter(sotilgan=True)
    
    # Pagination
    paginator = Paginator(mahsulotlar, 12)  # Har sahifada 12 ta mahsulot
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    return render(request, 'mening_elonlarim.html', {
        'mahsulotlar': page_obj,
        'page_obj': page_obj
    })

@login_required
def sotilgan_qilish_view(request, mahsulot_id):
    mahsulot = get_object_or_404(Mahsulot, id=mahsulot_id, user=request.user)
    mahsulot.sotilgan = True
    mahsulot.save()
    messages.success(request, f'"{mahsulot.name}" sotilganlar ro\'yxatiga o\'tkazildi!')
    return redirect('mening_elonlarim')

@login_required
def elon_ochirish_view(request, mahsulot_id):
    mahsulot = get_object_or_404(Mahsulot, id=mahsulot_id, user=request.user)
    mahsulot_name = mahsulot.name
    mahsulot.delete()
    messages.success(request, f'"{mahsulot_name}" e\'loni o\'chirildi!')
    return redirect('mening_elonlarim')

@login_required
def sevimliga_qoshish_view(request, mahsulot_id):
    try:
        mahsulot = get_object_or_404(Mahsulot, id=mahsulot_id)
        
        # Mahsulot allaqachon sevimlilarda bormi tekshiramiz
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
    try:
        sevimlilar = Sevimli.objects.filter(user=request.user).order_by('-sana')
        return render(request, 'sevimlilar.html', {'sevimlilar': sevimlilar})
    except Exception as e:
        print(f"DEBUG: Xatolik - {e}")
        return render(request, 'sevimlilar.html', {'sevimlilar': []})

@login_required
def sevimlidan_ochirish_view(request, sevimli_id):
    try:
        sevimli = get_object_or_404(Sevimli, id=sevimli_id, user=request.user)
        mahsulot_nomi = sevimli.mahsulot.name
        sevimli.delete()
        messages.success(request, f'"{mahsulot_nomi}" sevimlilardan olib tashlandi')
        return redirect('sevimlilarim')
    except Exception as e:
        messages.error(request, f'Xatolik yuz berdi: {str(e)}')
        return redirect('sevimlilarim')