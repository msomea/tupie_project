from django.shortcuts import render, redirect, resolve_url
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Region, District, Ward, Place, Street, Item
from .forms import ItemForm
from django.http import JsonResponse

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
            messages.error(request, 'Please fix the errors below.')
    else:
        form = UserCreationForm()
    return render(request, 'tupie_app/signup.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        next_url = request.GET.get('next') or resolve_url('tupie_app:home')
        if user:
            auth_login(request, user)
            return redirect(next_url)
        else:
            messages.error(request, 'Invalid Username or Password.')
    return render(request, 'tupie_app/login.html')

def logout_view(request):
    auth_logout(request)
    return redirect('tupie_app:home')

def get_districts(request):
    region_id = request.GET.get('region')
    districts = District.objects.filter(region_id=region_id).values('district_code', 'district_name')
    return JsonResponse(list(districts), safe=False)

def get_wards(request):
    district_id = request.GET.get('district')
    wards = Ward.objects.filter(district_id=district_id).values('ward_code', 'ward_name')
    return JsonResponse(list(wards), safe=False)

def get_places(request):
    ward_id = request.GET.get('ward')
    places = Place.objects.filter(ward_id=ward_id).values('id', 'place_name')
    return JsonResponse(list(places), safe=False)

@login_required
def add_item(request):
    if request.method == 'POST':
        form = ItemForm(request.POST)
        if form.is_valid():
            item = form.save(commit=False)
            item.owner = request.user
            item.save()
            messages.success(request, 'Item added!')
            return redirect('tupie_app:home')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = ItemForm()

        # Force early evaluation of querysets to avoid lazy DB access in template
        try:
            _ = list(form.fields['district'].queryset)
            _ = list(form.fields['ward'].queryset)
            _ = list(form.fields['place'].queryset)
        except Exception as e:
            messages.error(request, f"Form initialization error: {e}")
            form.fields['district'].queryset = District.objects.none()
            form.fields['ward'].queryset = Ward.objects.none()
            form.fields['place'].queryset = Place.objects.none()

    regions = Region.objects.all()
    return render(request, 'tupie_app/add_item.html', {
        'form': form,
        'regions': regions
    })
