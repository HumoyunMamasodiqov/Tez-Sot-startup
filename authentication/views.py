from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.utils.dateparse import parse_date
from django.views.decorators.cache import never_cache
from .models import Profile
import re


@never_cache
def kirish_view(request):
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        identifier = request.POST.get('identifier', '').strip()
        password = request.POST.get('password', '').strip()

        if not identifier or not password:
            messages.error(request, "Iltimos, ism/email/telefon va parolni kiriting.")
            return render(request, 'kirish.html', {'identifier': identifier})

        user = None

        # 1️⃣ Email orqali qidirish
        try:
            user = User.objects.get(email__iexact=identifier)
        except User.DoesNotExist:
            pass

        # 2️⃣ Username orqali qidirish
        if user is None:
            try:
                user = User.objects.get(username__iexact=identifier)
            except User.DoesNotExist:
                pass

        # 3️⃣ Ism orqali qidirish
        if user is None:
            try:
                user = User.objects.get(first_name__iexact=identifier)
            except User.DoesNotExist:
                pass

        # 4️⃣ Telefon orqali qidirish
        if user is None:
            digits = re.sub(r'\D', '', identifier)
            if len(digits) >= 9:
                last9 = digits[-9:]
                try:
                    for profile in Profile.objects.all():
                        clean_db_phone = re.sub(r'\D', '', profile.phone)
                        if clean_db_phone.endswith(last9):
                            user = profile.user
                            break
                except Exception:
                    pass

        if user is None:
            messages.error(request, "Foydalanuvchi topilmadi. Iltimos, ism, email yoki telefonni to'g'ri kiriting.")
            return render(request, 'kirish.html', {'identifier': identifier})

        # Parolni tekshirish
        user_auth = authenticate(request, username=user.username, password=password)
        if user_auth is None:
            messages.error(request, "Parol noto'g'ri. Iltimos, qayta urinib ko'ring.")
            return render(request, 'kirish.html', {'identifier': identifier})

        # Kirish muvaffaqiyatli
        login(request, user_auth)
        messages.success(request, f"Xush kelibsiz, {user.first_name or user.username}!")
        return redirect('home')

    return render(request, 'kirish.html')


@never_cache
def chiqish_view(request):
    if request.user.is_authenticated:
        logout(request)
        messages.success(request, "Siz tizimdan chiqdingiz!")
    return redirect('/')


@never_cache
def signup_view(request):
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        ism = request.POST.get('firstName', '').strip()
        familya = request.POST.get('lastName', '').strip()
        email = request.POST.get('email', '').strip()
        parol = request.POST.get('password', '').strip()
        tugilgan_sana = request.POST.get('birthDate', '').strip()
        telefon = request.POST.get('phone', '').strip()

        # Barcha maydonlarni tekshirish
        if not ism:
            messages.error(request, "Ism maydoni bo'sh bo'lishi mumkin emas.")
            return render(request, 'signup.html')
        if not familya:
            messages.error(request, "Familiya maydoni bo'sh bo'lishi mumkin emas.")
            return render(request, 'signup.html')
        if not email:
            messages.error(request, "Email maydoni bo'sh bo'lishi mumkin emas.")
            return render(request, 'signup.html')
        if not parol:
            messages.error(request, "Parol maydoni bo'sh bo'lishi mumkin emas.")
            return render(request, 'signup.html')
        if not tugilgan_sana:
            messages.error(request, "Tug'ilgan sana maydoni bo'sh bo'lishi mumkin emas.")
            return render(request, 'signup.html')
        if not telefon:
            messages.error(request, "Telefon maydoni bo'sh bo'lishi mumkin emas.")
            return render(request, 'signup.html')

        # Email va telefon unikalligini tekshirish
        if User.objects.filter(email=email).exists():
            messages.error(request, "Bu email allaqachon ro'yxatdan o'tgan.")
            return render(request, 'signup.html')

        if Profile.objects.filter(phone=telefon).exists():
            messages.error(request, "Bu telefon raqami allaqachon ro'yxatdan o'tgan.")
            return render(request, 'signup.html')

        try:
            # Foydalanuvchi yaratish
            user = User.objects.create_user(
                username=email,
                first_name=ism,
                last_name=familya,
                email=email,
                password=parol,
                is_active=True
            )

            # Profil yaratish
            Profile.objects.create(
                user=user,
                birth_date=parse_date(tugilgan_sana),
                phone=telefon
            )

            # Avtomatik kirish
            login(request, user)
            messages.success(request, f"Xush kelibsiz, {ism}!")
            return redirect('home')
                
        except Exception as e:
            messages.error(request, f"Ro'yxatdan o'tishda xatolik yuz berdi: {str(e)}")
            return render(request, 'signup.html')

    return render(request, 'signup.html')


@never_cache
def home_view(request):
    if not request.user.is_authenticated:
        return redirect('kirish')
    return render(request, 'home.html')