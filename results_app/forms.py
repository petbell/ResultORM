from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms  import AuthenticationForm
from django.forms import fields


class ContactForm (forms.Form):
    name = forms.CharField(label="Your name", max_length=30, widget=forms.TextInput(attrs={'class':'formtext'}))
    email = forms.EmailField( widget=forms.TextInput(attrs={'class':'formtext'}))
    mobile = forms.IntegerField( widget=forms.TextInput(attrs={'class':'formtext'}))


class ResultForm (forms.Form):
    studentid = forms.IntegerField(label="Student Number", widget=forms.TextInput(attrs={'class':'formtext'}))
    cardpin = forms.IntegerField(label="Card PIN", widget=forms.TextInput(attrs={'class':'formtext'}))
    serial = forms.IntegerField(label="Card Serial Number", widget=forms.TextInput(attrs={'class':'formtext'}))
    
    
class LoginForm(AuthenticationForm):
    username = forms.CharField(max_length=30, widget=forms.TextInput())
    password = forms.CharField(max_length=30,widget=forms.PasswordInput ())      
    
    
    class Meta:
        model = User
        fields = ['username', 'password']

class SignUpForm(forms.ModelForm):
    first_name = forms.CharField(max_length=30, widget=forms.TextInput(attrs={'class':'formtext'}))
    last_name = forms.CharField(max_length=30, widget=forms.TextInput(attrs={'class':'formtext'}))
    username = forms.CharField(max_length=30, widget=forms.TextInput(attrs={'class':'formtext'}))
    email = forms.EmailField(max_length=30, widget=forms.EmailInput(attrs={'class':'formtext'}))
    password = forms.CharField(max_length=30, widget=forms.PasswordInput(attrs={'class':'formtext'}))
    confirm_password = forms.CharField(max_length=30, widget=forms.PasswordInput(attrs={'class':'formtext'}))
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username',  'email', 'password']


class CardForm (forms.Form):
    number_of_card = forms.IntegerField (label="Number of Cards")
    
    