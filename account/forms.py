from django.contrib.auth.forms import UserCreationForm, UserChangeForm
# from django.contrib.auth.models import User
from django.conf import settings
from django import forms
from account.models import User

class SignUpForm(UserCreationForm):

    email = forms.EmailField()
    
    class Meta:
        model = User #settings.AUTH_USER_MODEL
        fields = ('username', 'email', 'password1', 'password2')



class EditProfileForm(UserChangeForm):
    username = forms.CharField(max_length=100, widget=forms.TextInput())
    first_name = forms.CharField(max_length=100, widget=forms.TextInput())
    first_name = forms.CharField(max_length=100, widget=forms.TextInput())
    email = forms.EmailField()
    
    class Meta:
        model = User #settings.AUTH_USER_MODEL
        fields = ('username', 'first_name', 'last_name', 'email', 'bio', 'pic')
        