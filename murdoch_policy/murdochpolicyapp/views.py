from django.shortcuts import render
from django.http import HttpResponse


# Create your views here.
def index(request):
    return render(request, 'index.html')


def upload(request):
    return render(request, 'upload-policy.html')


def search(request):
    return render(request, 'search-policy.html')


def browse(request):
    return render(request, 'browse-policy.html')
