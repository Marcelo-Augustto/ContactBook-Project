from django.shortcuts import render, redirect
from django.contrib import messages, auth
from django.core.validators import validate_email
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from .models import FormContact


def login(request):
    if request.method != 'POST':
        return render(request, 'accounts/login.html')
    
    username = request.POST.get('username')
    password = request.POST.get('password')

    user = auth.authenticate(request, username=username, password=password)

    if not user:
        messages.error(request, 'Invalid credentials')
        return render(request, 'accounts/login.html')
    else:
        auth.login(request, user)
        messages.success(request, 'You logged in')
        return redirect('index')


def logout(request):
    auth.logout(request)
    return redirect('dashboard')


def register(request):
    if request.method != 'POST':
        messages.info(request, 'Nothing was posted')
        return render(request, 'accounts/register.html')

    username = request.POST.get('username')
    email = request.POST.get('email')
    password = request.POST.get('password')
    password_confirm = request.POST.get('password_confirm')

    if not username or not email or not password or not password_confirm:
        messages.error(request, 'All fields must be filled')
        return render(request, 'accounts/register.html')

    try:
        validate_email(email)
    except:
        messages.error(request, 'Invalid email')
        return render(request, 'accounts/register.html')
    
    if password != password_confirm:
        messages.error(request, 'Passwords do not match')
        return render(request, 'accounts/register.html')

    if User.objects.filter(username=username).exists():
        messages.error(request, 'Username already exists')
        return render(request, 'accounts/register.html')
    
    if User.objects.filter(email=email).exists():
        messages.error(request, 'Email already exists')
        return render(request, 'accounts/register.html')
        
    messages.success(request, 'The user has been registered successfully')

    user = User.objects.create_user(username=username, email=email, password=password)
    user.save()
    return redirect('login')

@login_required(redirect_field_name='login')
def dashboard(request):
    if request.method != 'POST':
        form = FormContact()
        return render(request, 'accounts/dashboard.html', {'form': form})

    form = FormContact(request.POST, request.FILES)

    if not form.is_valid():
        messages.error(request, 'An error has occurred')
        form = FormContact(request.POST)
        return render(request, 'accounts/dashboard.html', {'form': form})
    
    form.save()
    messages.success(request, f'Contact {request.POST.get("name")} was registered.')
    return redirect('dashboard')
