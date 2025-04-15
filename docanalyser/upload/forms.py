from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class UploadFileForm(forms.Form):
    file = forms.FileField()

from django import forms

class DeleteDocumentForm(forms.Form):
    document_id = forms.IntegerField(
        label='ID документа для удаления',
        min_value=1,
        widget=forms.NumberInput(attrs={'class': 'form-control'}))
