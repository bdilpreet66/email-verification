from django import forms
from django.contrib.auth.models import User
from django.core.validators import EmailValidator
from .models import Questions,Articles,Report

class AskAnyThing(forms.ModelForm):
    email = forms.CharField(widget=forms.EmailInput(),validators=[EmailValidator])
    question = forms.CharField(widget=forms.Textarea())

    class Meta:
        model = Questions
        fields = ['email','question']

class CreateNewForm(forms.ModelForm):
    pics = forms.FileField(widget=forms.ClearableFileInput())

    class Meta():
        model = Articles
        fields = ['title','content','pics']

class EditForm(forms.ModelForm):
    pics = forms.FileField(widget=forms.ClearableFileInput())
    class Meta():
        model = Articles
        fields = ['content','pics']

class QuestionForm(forms.ModelForm):

    class Meta():
        model = Questions
        fields = ['answer']

class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('email','first_name','last_name')

class ReportForm(forms.ModelForm):
    email = forms.CharField(widget=forms.EmailInput(),validators=[EmailValidator])
    description = forms.CharField(widget=forms.Textarea())

    class Meta:
        model = Report
        fields = ['topic','description','email']