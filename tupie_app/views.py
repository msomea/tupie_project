from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages

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
