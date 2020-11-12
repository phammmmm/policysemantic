from django import forms
from bootstrap_datepicker_plus import DatePickerInput
from murdochpolicyapp.models import Document


class DocumentForm(forms.ModelForm):
    class Meta:
        model = Document
        fields = ('title', 'version', 'category','document_type', 'owner', 'document_file','created_date','last_review_date','review_interval','next_review_date')
        widgets = {
            'title': forms.TextInput(attrs={'class': 'col-12 col-12-xsmall'}),
            'created_date': DatePickerInput(),
            'last_review_date': DatePickerInput(),
            'next_review_date': DatePickerInput(),
        }
        labels = {
            'title': 'Document Title',
            'version': 'Version',
            'category': 'Document Category',
            'document_type': 'Document Type',
            'owner': 'Owner',
            'document_file': 'Document File',
            'created_date':'Created Date',
            'last_review_date': 'Last Review Date',
            'review_interval': 'Review Interval',
            'next_review_date': 'Next Review Date',
        }


      