from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required


# Create your views here.
@login_required(login_url='/admin/login/')
def index(request):
    if request.user.is_superuser:
        return render(request, 'index.html')
    return render(request, 'staff/index.html')

def upload(request):
    return render(request, 'upload-policy.html')

def search(request):
    return render(request, 'search-policy.html')

def browse(request):
    return render(request, 'browse-policy.html')

def login(request):
    return render(request, 'accounts/login.html')

def staffIndex(request):
    return render(request, 'staff/index.html')

def staffSearch(request):
    return render(request, 'staff/search-policy.html')

def staffBrowse(request):
    return render(request, 'staff/browse-policy.html')
