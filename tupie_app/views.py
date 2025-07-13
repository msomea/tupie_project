from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Region, District, Ward, Place, Street, Item
from .forms import ItemForm, UserCreationForm

def home(request):
    return render(request, 'tupie_app/home.html')

def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Account Created! Please log in.')
            return redirect('tupie_app:login')
    else:
        form = UserCreationForm()
    return render(request, 'tupie_app/signup.html', {'form': form})

def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('tupie_app:home')
        else:
            messages.error(request, 'Invalid Username or Password.')
    return render(request, 'tupie_app/login.html')

def logout(request):
    logout(request)
    return redirect('tupie_app:home')

@login_required
def add_item(request):
    regions = Region.objects.all()
    if request.method == 'POST':
        form = ItemForm(request.POST)
        if form.is_valid():
            item = form.save(commit=False)
            item.owner = request.user
            item.save()
            messages.success(request, 'Item added!')
            return redirect('tupie_app:home')
    else:
        form = ItemForm()
    return render(request, 'tupie_app/add_item.html', {'form': form, 'regions': regions})
