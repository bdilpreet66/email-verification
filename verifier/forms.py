from .models import Documents
from django import forms
from django.core.validators import FileExtensionValidator



class SingleForm(forms.ModelForm):
    email = forms.CharField(widget=forms.EmailInput())
    
    class Meta:
        model = Documents
        fields = ['email',]


class ListForm(forms.ModelForm):
    email = forms.CharField(widget=forms.EmailInput(),help_text='You will recieve a download link on this email')
    doc_name = forms.FileField(validators=[FileExtensionValidator(allowed_extensions=['csv'],message='only csv files are allowed')])
    class Meta:
        model = Documents
        fields = ['email','doc_name']