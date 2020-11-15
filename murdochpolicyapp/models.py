from __future__ import unicode_literals

import os
from django.db import models
from django.contrib import auth,admin
from django.contrib.auth.models import User
from django.core.files.storage import FileSystemStorage
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator
from django.utils import timezone

def validate_file_extension(value):
    ext = os.path.splitext(value.name)[1]  # [0] returns path+filename
    valid_extensions = ['.pdf']
    if not ext.lower() in valid_extensions:
        raise ValidationError('Unsupported file extension.')

def get_path(instance,filename):
    name = instance.title.replace(' ','_').title()+'.pdf'
    return os.path.join('policy_documents',name)

# Create your models here.
class Category(models.Model):
    category_name = models.CharField(max_length=200,unique=True)
    class Meta:
        ordering = ["-category_name"]

    def __str__(self):
        return self.category_name
        
class DocumentType(models.Model):
    document_type = models.CharField(max_length=200,unique=True)
    class Meta:
        ordering = ["-document_type"]

    def __str__(self):
        return self.document_type

class StopWord(models.Model):
    value = models.CharField(max_length=200,primary_key=True)


class OverwriteStorage(FileSystemStorage):
    def get_available_name(self, name):
        if self.exists(name):
            os.remove(os.path.join(settings.MEDIA_ROOT, name))
        return name

# Create document models
class Document(models.Model):
    title = models.CharField(max_length=200)
    version = models.IntegerField(default=1, validators=[MinValueValidator(1)])
    owner = models.ForeignKey(User,on_delete=models.CASCADE)
    category = models.ForeignKey(Category,on_delete=models.CASCADE)
    document_type = models.ForeignKey(DocumentType,on_delete=models.CASCADE)
   
    created_date = models.DateTimeField()
    last_modified_date = models.DateTimeField(auto_now=True)
    last_review_date = models.DateTimeField()
    review_interval = models.IntegerField(default=1,validators=[MinValueValidator(1)])
    next_review_date = models.DateTimeField()
    document_size = models.IntegerField(default=1)
    document_text = models.TextField()
    feature_words = models.TextField()
    document_file = models.FileField(blank=True, max_length=256, upload_to=get_path, validators=[validate_file_extension])
    related_documents =[]
    class Meta:
        ordering = ["-title"]

    def __str__(self):
        return self.title
    

# Create DocLink
class DocumentLink(models.Model):
    source = models.ForeignKey(Document,related_name='documentSource',on_delete=models.CASCADE)
    target = models.ForeignKey(Document,related_name='documentTarget',on_delete=models.CASCADE)
    value = models.FloatField() 

class Reminder(models.Model):
    user = models.ForeignKey(auth.models.User, on_delete=models.CASCADE)
    document = models.ForeignKey(Document, on_delete=models.CASCADE)
