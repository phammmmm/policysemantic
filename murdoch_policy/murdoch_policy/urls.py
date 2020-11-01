"""murdoch_policy URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from murdochpolicyapp import views
#from murdochpolicyapp.views import index
from django.conf.urls import include
from django.conf.urls import url
from django.contrib.auth import views as auth_views
from django.views.generic.base import TemplateView # new

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('murdochpolicyapp.urls')),
    path('murdochpolicyapp/', include('django.contrib.auth.urls')), 
#    url(r'^admin/$', index, name='index'),
#    path('murdochpolicyapp/login', auth_views.LoginView.as_view()),
#    path('murdochpolicyapp/', include('murdochpolicyapp.urls')),
#    path('', views.index, name='index'),
#    path('', TemplateView.as_view(template_name='home.html'), name='home'), # new
#    path('', admin.site.urls), # new
#    url(r'^$', TemplateView.as_view(template_name='home.html'), name='home'),
#    url(r'^login/$', auth_views.login, {'template_name': 'login.html'}, name='login'),
#    url(r'^logout/$', auth_views.logout, {'template_name': 'logged_out.html'}, name='logout'),
]
