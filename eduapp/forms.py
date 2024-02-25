from django import forms
from .models import Question,Answer,Quiz,QuizQuestion
from ckeditor.widgets import CKEditorWidget
from django.forms.widgets import Textarea




class CKEditorWidget(Textarea):
    template_name = 'Que/question.html'

class CreateUserForm(forms.Form):
    first_name=forms.CharField(widget=forms.TextInput(attrs={'class':'form-control mt-2','placeholder':'firstname'}))
    last_name=forms.CharField(widget=forms.TextInput(attrs={'class':'form-control mt-2','placeholder':'lastname'}))
    username = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control mt-2','placeholder':'username'}),required=True)
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class':'form-control mt-2','placeholder':'email'}),required=True)
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control mt-2','placeholder':'password'}),required=True)
    password_repeat = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control mt-2','placeholder':'confirm password'}))

class QuestionsForm(forms.ModelForm):
    class Meta:
        model=Question
        fields = ['query']
        widget={'query':CKEditorWidget()}
        
class AnswerForm(forms.ModelForm):
    class Meta:
        model=Answer
        fields=['ans']

class QuizCreationForm(forms.ModelForm):
    class Meta:
        model = Quiz
        fields = ['name', 'number_of_questions', 'time', 'required_score_to_pass']