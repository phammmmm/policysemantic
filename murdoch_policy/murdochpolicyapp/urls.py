from django.urls import path
from murdochpolicyapp import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('', views.index, name='index'),
    path('upload/', views.upload, name='upload'),
    path('search/', views.search, name='search'),
    path('browse/', views.browse, name='browse'),
    path('registration/login/', views.login, name='login'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
