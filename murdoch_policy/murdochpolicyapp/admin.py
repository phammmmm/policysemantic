from django.contrib import admin
from django.contrib.auth.models import Group
# Register your models here.
#from . import models
from .models import Category

admin.site.site_header = 'Murdoch Policy Index'
admin.site.site_title = 'Murdoch'
admin.site.unregister(Group)
admin.site.register(Category)
