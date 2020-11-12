from django.urls import path,include
from django.contrib import admin
from django.contrib.auth import views as auth_views
from murdochpolicyapp.views import CategoryList,DocumentList,DocumentDetailView

urlpatterns = [
    path('document/<int:pk>/', DocumentDetailView.as_view(), name='document-detail'),
]