from django.contrib import admin
from .models import Category, Document,DocumentType, DocumentLink,StopWord, Reminder

# Register your models here.
admin.site.register(Category)
admin.site.register(DocumentType)
admin.site.register(Document)
admin.site.register(DocumentLink)
admin.site.register(StopWord)
admin.site.register(Reminder)