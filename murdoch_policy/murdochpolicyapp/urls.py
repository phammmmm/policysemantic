from django.urls import path
from murdochpolicyapp import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('', views.index, name='index'),
    path('upload/', views.upload, name='upload'),
    path('search/', views.search, name='search'),
    path('browse/', views.browse, name='browse'),
    path('accounts/login/', views.login, name='login'),
    path('staff/index/', views.staffIndex, name='staffIndex'),
    path('staff/search/', views.staffSearch, name='staffSearch'),
    path('staff/browse/', views.staffBrowse, name='staffBrowse'),
]
#+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
