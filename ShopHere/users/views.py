from django.contrib.auth import login, authenticate
from .forms import UserProfileForm,UserLoginForm
from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponse,Http404
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm

def signup(request):
    if request.method == 'POST':
        form = UserProfileForm(data=request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return JsonResponse({'status': 'OK'})
        return JsonResponse({'errors': form.errors,'status': ''})
    else:
        form = UserProfileForm()
    return HttpResponse(form.as_p())


def login1(request):
    if request.method == 'POST':
        form = UserLoginForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=raw_password)
            if user == None:
                return JsonResponse({'errors': 'Please enter a valid username and password. Note that both fields may be case-sensitive.','status': ''})
            login(request, user)
            return JsonResponse({'status': 'OK'})
        return JsonResponse({'errors': 'Please enter a valid username and password. Note that both fields may be case-sensitive.','status': ''})
    else:
        form = UserLoginForm()
    return HttpResponse(form.as_p())


def home(request):
    return render(request, 'users/home.html', {})
