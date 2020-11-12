from murdochpolicyapp.models import Category,DocumentLink,Document,DocumentType,Reminder
from django.urls import reverse
from django.views.generic import (TemplateView,ListView,
                                  DetailView,CreateView,
                                  UpdateView,DeleteView)
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import AuthenticationForm
from murdochpolicyapp import utils
from django.db.models import Q
from django.conf import settings
from django.contrib.auth.decorators import login_required

import asyncio
import os

from murdoch_policy import settings
from django.shortcuts import render

from murdochpolicyapp.forms import DocumentForm

@login_required(login_url='/admin/login/')
def index(request):
    if request.user.is_authenticated:
        return render(request, 'index.html')


class SearchPage(ListView):
    template_name = 'search-policy.html'
    model = Document
    def get_queryset(self):
        query = self.request.GET.get('q')
        if not query:
            query = ""
            object_list =[]
        else:
            object_list = Document.objects.filter(Q(title__icontains=query))
        return object_list


class BrowsePage(ListView):
    template_name = 'browse-policy.html' 
    model = Category
    context_object_name = 'name'
    queryset = Category.objects.all()
    def get_context_data(self, **kwargs):
        context = super(BrowsePage,self).get_context_data(**kwargs)
        context["documents"] = Document.objects.all()
        context["categories"] = self.queryset 
        return context
   
       

class UploadPage(TemplateView):
    template_name = 'upload-policy.html'
    model = Category
    context_object_name = 'name'
    
    def get_context_data(self, **kwargs):
        context = super(UploadPage,self).get_context_data(**kwargs)
        context["categories"] = Category.objects.all()
        return context
    def get(self,request,*args, **kwargs):
        form = DocumentForm(request.POST, request.FILES)
        return render(request, 'upload-policy.html', {'form': form})

    def post(self,request,*args, **kwargs):
        form = DocumentForm(request.POST, request.FILES)
        if request.method == 'POST':
            if form.is_valid():

                #Clean up file or document with same title
                title = form.cleaned_data['title'].strip()
                file_name = os.path.join(settings.DOC_DIR,title.replace(' ','_')+'.pdf')
                if(os.path.isfile(file_name)):
                    os.remove(file_name)
                docs = Document.objects.filter(title__exact=title)
                if(len(docs)>0):
                    for doc in docs: 
                        utils.removeDocument(doc)
                
                obj = form.save()

                #Updating relationship fields
                text = utils.pdf_to_txt(file_name)
                obj.document_text=text
                obj.feature_words = utils.get_feature_words(text)
                obj.document_size =len(text)
                obj.save()
                #create doc links
                utils.createDocLinks(obj)
                #set reminder
                reminder = Reminder.objects.create(user=request.user,document=obj)
                reminder.save()
                #refresh the home page document network 
                utils.refreshHomeGraph()
                #redirect to document details page
                return HttpResponseRedirect("/murdochpolicyapp/document/{id}/".format(id= obj.id))
                # return render(request, 'upload-policy.html', {'form': form})
            else:
                form = DocumentForm(request.POST, request.FILES)
                return render(request, 'upload-policy.html', {'form': form})
                    
        
    


class CategoryList(ListView):
    model = Category

class DocumentList(ListView):
    model = Document

class DocumentDetailView(DetailView):
    model = Document

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
       
        return context
    def get_object(self):
        obj = super().get_object()
        obj.relatedDocs = utils.getRelatedDoc(obj)
        utils.draw_doc_relationship(obj)
        return obj

