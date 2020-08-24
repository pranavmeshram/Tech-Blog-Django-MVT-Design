# Contact Us:
#     Name
#     Email
#     Contact Number
#     Submit

from django import forms
import re
from blog.models import Category, Post
# from django_summernote.widgets import SummernoteWidget, SummernoteInplaceWidget
from django.utils.text import slugify
from django.core.exceptions import ObjectDoesNotExist


class ContactUsForm(forms.Form):
    name = forms.CharField(max_length = 100, widget = forms.TextInput(attrs={'placeholder':'100 characters max.'}))
    email = forms.EmailField(required = False, widget = forms.EmailInput(attrs={'placeholder':'Enter your email'}))
    phone_number = forms.RegexField(required = False, regex= "^[6-9]\d{9}$", widget = forms.TextInput(attrs={'placeholder':'Only 10 digits allowed'}))
    message = forms.CharField(widget=forms.Textarea(attrs={'placeholder':'If you have any message for us, please type it here' }), required = False)

    # Only email or phone_number must be entered.
    def clean(self):
        cleaned_data = super().clean()
        if not (cleaned_data.get('email') or cleaned_data.get('phone_number')):
            raise forms.ValidationError("Please enter either Email or Phone Number Correctly", code="invalid")

    def clean_email(self):
        data = self.cleaned_data['email']
        if ("edyoda" not in data) and (data != ''):
            raise forms.ValidationError("Invalid domain", code="invalid")
        return data 


class RegisterForm(forms.Form):
    
    username = forms.CharField(max_length=100, help_text='Username should be between 2-8 chars. Only "@" and "_" special characters are allowed.',
                                widget= forms.TextInput(attrs={'placeholder':'Enter your username name'}))
    password = forms.CharField(max_length=32, min_length=2, widget = forms.PasswordInput, help_text='''Password should have minimum of 3 characters and should have atleast 1 of each
                                        UPPER case, lower CASE, special character and numeric character.''')
    confirm_password = forms.CharField(max_length=32, min_length=2, widget = forms.PasswordInput(attrs={'placeholder':'Please confirm your password'}))

    GENDER_CHOICES = [("M","Male"), ("F","Female")]
    gender = forms.ChoiceField(choices = GENDER_CHOICES, widget = forms.RadioSelect)


    def clean(self):  # Password and confirm Password should be same.
        cleaned_data = super().clean()
        if (cleaned_data.get('password') != cleaned_data.get('confirm_password')):
            raise forms.ValidationError("Password and Confirm Password do not match !!!", code="Mismatch_Password")


    def clean_username(self):
        data = self.cleaned_data['username']

        pattern = "^[\w@]{2,8}$"
        result = re.match(pattern, data)

        if not result:
            raise forms.ValidationError('''Invalid Username!''', code="invalid")
        return data 


    def clean_password(self):
        data = self.cleaned_data['password']

        pattern = "^(?=.*[    )(?=.*[A-Z])(?=.*\d)(?=.*[@#$!%*?&])[A-Za-z\d@#$!%*?&]{8,}$"
        result = re.match(pattern, data)

        if not result:
            raise forms.ValidationError('''Password pocily has not met!''', code="invalid")
        return data 


# class PostForm(forms.Form):
#     statuses = [("D","Draft"), ("P","Published")]

#     title = forms.CharField(max_length=250)
#     content = forms.CharField(widget=SummernoteWidget())
#     status = forms.ChoiceField(choices=statuses)
#     category = forms.ModelChoiceField(queryset= Category.objects.all())
#     image = forms.ImageField(required=False)


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields =['title', 'content', 'status', 'category', 'image']

    def clean_title(self):
        title = self.cleaned_data.get('title')
        slug = slugify(title)
        try:
            post_obj = Post.objects.get(slug = slug)
            raise forms.ValidationError("Slug already exists!", code="Invalid_Title")
        except ObjectDoesNotExist:
            return title

    # def clean_image(self): #image size less then 1 MB
    #     pass

class PostUpdateForm(PostForm):

    def clean_title(self):
        title = self.cleaned_data.get('title')
        return title