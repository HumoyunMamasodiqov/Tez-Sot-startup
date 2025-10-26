from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.utils.dateparse import parse_date
from .models import Profile
from django.views.decorators.cache import never_cache
from django.utils.decorators import method_decorator

@never_cache
def kirish_view(request):
    # Agar foydalanuvchi allaqachon kirgan bo'lsa, home sahifasiga yo'naltirish
    if request.user.is_authenticated:
        return redirect('home')
        
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        # Foydalanuvchini tekshirish
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            messages.success(request, f"Xush kelibsiz, {user.first_name}!")
            return redirect('home')
        else:
            messages.error(request, "Login yoki parol noto'g'ri!")
    
    # Clear any cached data
    response = render(request, 'kirish.html')
    response['Cache-Control'] = 'no-cache, no-store, must-revalidate'
    response['Pragma'] = 'no-cache'
    response['Expires'] = '0'
    return response

@never_cache
def chiqish_view(request):
    if request.user.is_authenticated:
        logout(request)
        messages.success(request, "Siz tizimdan chiqdingiz!")
    
    response = redirect('home')
    response['Cache-Control'] = 'no-cache, no-store, must-revalidate'
    response['Pragma'] = 'no-cache'
    response['Expires'] = '0'
    return response

@never_cache
def signup_view(request):
    # Agar foydalanuvchi allaqachon kirgan bo'lsa, home sahifasiga yo'naltirish
    if request.user.is_authenticated:
        return redirect('home')
        
    if request.method == 'POST':
        ism = request.POST.get('firstName')
        familya = request.POST.get('lastName')
        email = request.POST.get('email')
        parol = request.POST.get('password')
        tugilgan_sana = request.POST.get('birthDate')
        telefon = request.POST.get('phone')

        # Maydonlarni tekshirish
        if not all([ism, familya, email, parol, tugilgan_sana, telefon]):
            messages.error(request, "Barcha maydonlarni to'ldiring.")
            return render(request, 'login.html')

        # Foydalanuvchi mavjudligini tekshirish
        if User.objects.filter(email=email).exists():
            messages.error(request, "Bu elektron pochta allaqachon ro'yxatdan o'tgan.")
            return render(request, 'login.html')

        # Foydalanuvchini yaratish
        user = User.objects.create_user(
            username=email,
            first_name=ism,
            last_name=familya,
            email=email,
            password=parol
        )
        user.save()

        # Profile ma'lumotlarini saqlash
        Profile.objects.create(
            user=user,
            birth_date=parse_date(tugilgan_sana),
            phone=telefon
        )

        # Foydalanuvchini login qilish
        user = authenticate(request, username=email, password=parol)
        if user is not None:
            login(request, user)
            messages.success(request, "Hisob muvaffaqiyatli yaratildi!")
            return redirect('home')
        else:
            messages.error(request, "Kirishda xatolik yuz berdi.")
            return redirect('login')

    response = render(request, 'login.html')
    response['Cache-Control'] = 'no-cache, no-store, must-revalidate'
    response['Pragma'] = 'no-cache'
    response['Expires'] = '0'
    return response

@never_cache
def home_view(request):
    if not request.user.is_authenticated:
        return redirect('login')
    
    response = render(request, 'home.html')
    response['Cache-Control'] = 'no-cache, no-store, must-revalidate'
    response['Pragma'] = 'no-cache'
    response['Expires'] = '0'
    return response