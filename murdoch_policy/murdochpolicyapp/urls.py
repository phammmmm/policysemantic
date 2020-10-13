from django.urls import path
from murdochpolicyapp import views
from django.conf import settings
from django.conf.urls.static import static


app_name = 'murdochpolicyapp'

urlpatterns = [
    path('', views.index, name='index'),
    path('', views.upload, name='upload'),
    path('', views.search, name='search'),
    path('', views.browse, name='browse'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
