#Import
import os
import fnmatch
import re
from io import StringIO
import numpy as np
import sys
import networkx as nx
import matplotlib.pyplot as plt
import random
from datetime import datetime  
from datetime import timedelta 
import pandas as pd
import pytz

#Import DB Models
from murdochpolicyapp.models import Category, DocumentType ,DocumentLink,Document,StopWord,Reminder
from django.db.models import Q
from django.core.mail import send_mail
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404

#PDF Import
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfdocument import PDFDocument
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.pdfpage import PDFPage
from pdfminer.pdfparser import PDFParser
from pdfminer.pdftypes import resolve1
from pdfminer.psparser import PSLiteral, PSKeyword
from pdfminer.utils import decode_text

#NLTK
import nltk
nltk.download('stopwords')
nltk.download('punkt')
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import PorterStemmer

# Import all of the scikit learn stuff
import sklearn
from sklearn.decomposition import TruncatedSVD
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.preprocessing import Normalizer
from sklearn import metrics
from sklearn.cluster import KMeans, MiniBatchKMeans
from sklearn.model_selection import train_test_split
from sklearn.metrics import log_loss
import scipy

from murdoch_policy import settings

os.environ["DJANGO_ALLOW_ASYNC_UNSAFE"] = "true"
plt.switch_backend('Agg')

#Find files in folder matching pattern case insensitive
def findfiles(which, where='.'):
    rule = re.compile(fnmatch.translate(which), re.IGNORECASE)
    return [where+'/'+name for name in os.listdir(where) if rule.match(name)]

#Preprocessing - Convert lower case
def convert_lower_case(data):
    return np.char.lower(data)

#Preprocessing - Remove Stop words
def remove_stop_words(data):
    stop_words = stopwords.words('english')
    
    #Extend Stopwords
    policy_stop_words = []
    for word in StopWord.objects.all():
        policy_stop_words.append(word.value)
    
    words = word_tokenize(str(data))
    new_text = ""
    for w in words:
        if w not in policy_stop_words  and w not in stop_words and len(w) > 3: #remove also the word with length <= 2
            new_text = new_text + " " + w
    return new_text

#Preprocessing - Remove Punctuation
def remove_punctuation(data):
    symbols = "!\"#$%&()*+-./:;<=>?@[\]^_`{|}~\n"
    for i in range(len(symbols)):
        data = np.char.replace(data, symbols[i], ' ')
        data = np.char.replace(data, "  ", " ")
    data = np.char.replace(data, ',', '')
    return data

#Preprocessing - Remove Apostrophe
def remove_apostrophe(data):
    return np.char.replace(data, "'", "")


#Preprocessing - Stemming
def stemming(data):
    stemmer= PorterStemmer()
    
    tokens = word_tokenize(str(data))
    new_text = ""
    for w in tokens:
        new_text = new_text + " " + stemmer.stem(w)
    return new_text

#Preprocessing - convert numbers
def convert_numbers(data):
    tokens = word_tokenize(str(data))
    new_text = ""
    for w in tokens:
        try:
            w = num2words(int(w))
        except:
            a = 0
        new_text = new_text + " " + w
    new_text = np.char.replace(new_text, "-", " ")
    return new_text

#Preprocessing Data
def preprocess(data):
    data = convert_lower_case(data)
    data = remove_punctuation(data) #remove comma seperately
    data = remove_apostrophe(data)
    data = remove_stop_words(data)
    data = convert_numbers(data)
    data = stemming(data)
    data = remove_punctuation(data)
    data = convert_numbers(data)
    data = stemming(data) #needed again as we need to stem the words
    data = remove_punctuation(data) #needed again as num2word is giving few hypens and commas fourty-one
    data = remove_stop_words(data) #needed again as num2word is giving stop words 101 - one hundred and one
    return data


def pdf_to_txt(pdfFileName):
    output_string = StringIO()
    with open(pdfFileName, 'rb') as pdf_file:
        parser = PDFParser(pdf_file)
        doc = PDFDocument(parser)
        rsrcmgr = PDFResourceManager()
        device = TextConverter(rsrcmgr, output_string, laparams=LAParams())
        interpreter = PDFPageInterpreter(rsrcmgr, device)
        for page in PDFPage.create_pages(doc):
            interpreter.process_page(page) 
    pdf_file.close()
    return preprocess(output_string.getvalue())

def get_similarity(text1, text2):
    #Setup vector
    vectorizer = TfidfVectorizer(min_df=1,stop_words="english")
    corpus = [text1,text2]
    #Transform for pairwise similarity
    tfidf = vectorizer.fit_transform(corpus)
    pairwise_similarity = tfidf * tfidf.T 
    return pairwise_similarity[(0,1)]

def get_feature_words(text):
    vectorizer = TfidfVectorizer(min_df=1,stop_words="english")
    corpus = [text]
    tfidf = vectorizer.fit_transform(corpus)
    return vectorizer.get_feature_names()

def draw_network_documents(docs,docLinks,img_path):
    G = nx.Graph(day="Stackoverflow")

    for doc in docs:
        G.add_node(doc.title, group=doc.category.id, nodesize=doc.document_size)

    for link in docLinks:       
        doc1 = Document.objects.get(pk=link.source)
        doc2 = Document.objects.get(pk=link.target)
        G.add_weighted_edges_from([(doc1.title, doc2.title, link.value)])
    
    cats = Category.objects.all()
    color_map = {}
    colors = [  '#eebcbc', '#72bbd0', '#91f0a1', '#629fff','#bcc2f2','#eebcbc', '#caf3a6',
              '#f09494', '#f1f0c0', '#d2ffe7', '#ffdf55', '#ef77aa', '#d6dcff', '#d2f5f0']
    for i in range(len(cats)):
        if i<len(colors) :
            color_map[cats[i].id] = colors[i] 
        else:
            color_map[cats[i].id] = "#"+''.join([random.choice('0123456789ABCDEF') for j in range(6)])

    plt.figure(figsize=(20,20))
    options = {
        'edge_color': '#FFDEA2',
        'width': 1,
        'with_labels': True,
        'font_weight': 'regular',
    }
  
    nodeColors = [color_map[G.nodes[node]['group']] for node in G]
    sizes = [G.nodes[node]['nodesize']/10 for node in G]

    nx.draw(G, node_color=nodeColors, node_size=sizes, pos=nx.spring_layout(G, k=0.45, iterations=30), **options)
    ax = plt.gca()
    ax.collections[0].set_edgecolor("#555555") 
    plt.savefig(img_path)
    #plt.show()

def draw_doc_relationship(doc):
    docs = []
    docs.append(doc)
    for link in DocumentLink.objects.filter(source__exact=doc.id):
        target = Document.objects.get(pk=link.target)
        docs.append(target)
    for link in DocumentLink.objects.filter(target__exact=doc.id):
        source = Document.objects.get(pk=link.source)
        docs.append(source)
        
    docLinks = DocumentLink.objects.filter(Q(source__exact=doc.id) | Q(target__exact=doc.id))
    image_path = os.path.join(settings.IMG_DIR,str(doc.id)+'.png')
    draw_network_documents(docs,docLinks,image_path)

def getRelatedDoc(doc):
    docs = []
    for link in DocumentLink.objects.filter(source__exact=doc.id):
        target = Document.objects.get(pk=link.target)
        docs.append([target.title,link.value])
    for link in DocumentLink.objects.filter(target__exact=doc.id):
        source = Document.objects.get(pk=link.source)
        docs.append([source.title,link.value])
    return docs

def refreshStopWords():
    #clean StopWords
    StopWord.objects.all().delete()

     #Extend Stopwords
    policy_stop_words = []
    with open(settings.STOP_WORD_FILE) as f:
      for line in f:
        policy_stop_words.extend(line.rstrip('\n').split(','))
    for word in policy_stop_words:
        w, created = StopWord.objects.get_or_create(value=word)
        if created:
            w.save()

def removeDocument(doc_obj):
    DocumentLink.objects.filter(source__exact=doc_obj.id).delete()
    DocumentLink.objects.filter(target__exact=doc_obj.id).delete()
    doc_obj.delete()
    
#Create DocLinks
def createDocLinks(doc_obj):
    docs = Document.objects.all()
    for i in range(len(docs)):    
        if(doc_obj.id!=docs[i].id):
            similarity = get_similarity(docs[i].document_text, doc_obj.document_text)
            if(similarity>settings.RELATED_ALPHA):
                doclink = DocumentLink.objects.create(source=docs[i].id,target=doc_obj.id,value=similarity)
                doclink.save()

def refreshHomeGraph():
    docs = Document.objects.all()
    docLinks = DocumentLink.objects.all()
    draw_network_documents(docs,docLinks,settings.HOMEPAGE_MAP)

def sendReminder(reminder):
    reminder_text = 'Dear '+ reminder.user.first_name + ' '+ reminder.user.last_name +',\n'
    reminder_text += 'Please review the '+reminder.document.title + ' version '+ str(reminder.document.version)+'.\n'
    reminder_text +='Last Review Date: '+reminder.document.last_review_date.strftime("%b %d %Y") +'.\n'
    reminder_text +='To be reviewed before '+reminder.document.next_review_date.strftime("%b %d %Y") +'.\n'
    reminder_text +='Sincerely yours,\n'
    reminder_text +='MurdochPolicyApp Team'
    send_mail(
        subject = 'Murdoch Policy Documents Review Reminder',
        message = reminder_text,
        from_email = 'im.lyaclip@gmail.com',
        recipient_list = [reminder.user.email,],
        auth_user = 'im.lyaclip@gmail.com',
        auth_password = 'lxhbrlgabhhbptif',
        fail_silently = False,
    )

def sendReminderBatch():
    reminders = Reminder.objects.all()
    for reminder in reminders:
        if (datetime.now(timezone.utc) > reminder.document.next_review_date) :
            sendReminder(reminder)

def refreshDocs():
    DocumentLink.objects.all().delete()
    Document.objects.all().delete()
     #Init Documents
    doc_data = pd.read_csv("policy_data.csv") 
    for i in range(len(doc_data)):
        title = doc_data['Title'][i].strip()
        version = int(doc_data['Version'][i])
        cat = Category.objects.get(category_name__exact=doc_data['Category'][i].strip())
        doctype = DocumentType.objects.get(document_type__exact=doc_data['DocumentType'][i].strip())
        usr = User.objects.get(username__exact=doc_data['Owner'][i].strip())
        date1 = datetime.strptime(doc_data['DateCreated'][i], '%d/%m/%Y').replace(tzinfo=pytz.UTC)
        date2 = datetime.strptime(doc_data['LastModified'][i], '%d/%m/%Y').replace(tzinfo=pytz.UTC)
        date3 = datetime.strptime(doc_data['LastReviewed'][i], '%d/%m/%Y').replace(tzinfo=pytz.UTC)
        date4 = datetime.strptime(doc_data['NextReview'][i], '%d/%m/%Y').replace(tzinfo=pytz.UTC)
        review_interval = int(doc_data['ReviewInterval'][i])
        file_name = os.path.join(settings.DOC_DIR,title.replace(' ','_')+'.pdf')
        text = pdf_to_txt(file_name)
        size = len(text)
        words = get_feature_words(text)

        doc = Document.objects.create(title=title, version=version, category=cat, document_type=doctype ,owner = usr, created_date=date1,last_modified_date=date2, last_review_date=date3, review_interval= review_interval, next_review_date = date4 , document_size=size, document_text=text,feature_words = words)

        link = os.path.join('policy_documents',title.replace(' ','_')+'.pdf')
        doc.document_file.name = link
        doc.save()
    
    #Create Document Links
    docs = Document.objects.all()
    for i in range(len(docs)):    
        for j in range(len(docs)):
            if i<j:
                similarity = get_similarity(docs[i].document_text, docs[j].document_text)
                if(similarity>settings.RELATED_ALPHA):
                    doclink = DocumentLink.objects.create(source=docs[i].id,target=docs[j].id,value=similarity)
                    doclink.save()
    #Redraw the documents network graph
    docLinks = DocumentLink.objects.all()
    print(len(docs))
    print(len(docLinks))
    draw_network_documents(docs,docLinks,settings.HOMEPAGE_MAP)

def refreshAll():
    #Clean up all tables
    DocumentType.objects.all().delete()
    Category.objects.all().delete()
    for user in User.objects.all():
        if(user.username != 'admin' and user.username != 'meo'):
            user.delete()
            
    #Init StopWords
    refreshStopWords()
    
    #Init Users
    user_data = pd.read_csv('user.csv')
    for i in range(len(user_data)):
        user = User.objects.create_user(user_data['UserName'][i].strip(), password='ict30208',first_name = user_data['FirstName'][i], last_name=user_data['LastName'][i], is_staff=True, is_superuser=True)
        user.save()
        
    #Init Categories
    cat_data = pd.read_csv("category.csv")
    for catname in cat_data['Category']:
        cat = Category.objects.create(category_name=catname.strip())
        cat.save()
    #Init Document Types
    dt_data = pd.read_csv("doc_type.csv")
    for dt in dt_data['doc_type']:
        doctype = DocumentType.objects.create(document_type=dt.strip())
        doctype.save()
    refreshDocs()
   

