from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from .models import Category

# Create your views here.
@login_required(login_url='/admin/login/')
def index(request):
    if request.user.is_superuser:
        return render(request, 'index.html')
    return render(request, 'staff/index.html')

def upload(request):
    return render(request, 'upload-policy.html')

def search(request):
    return render(request, 'search-policy.html', {'title':'Search'})

def browse(request):
    #policy_categories = Catergory.objects.all()[:10]
    policy_categories = Category.objects.all()

    context = {
    'policy_categories': policy_categories
    }

    return render(request, 'browse-policy.html', context)
    #return render(request, 'browse-policy.html')

def login(request):
    return render(request, 'accounts/login.html')

def staffIndex(request):
    return render(request, 'staff/index.html')

def staffSearch(request):
    return render(request, 'staff/search-policy.html')

def staffBrowse(request):
    policy_categories = Category.objects.all()

    context = {
    'policy_categories': policy_categories
    }
    return render(request, 'staff/browse-policy.html', context)
