# from django.contrib.auth.models import User  
# from django.forms.fields import EmailField  
# from django.forms.forms import Form  
from django.forms import ModelForm
from .models import Review, Renting
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Field
from crispy_forms.bootstrap import FormActions

class ReviewForm(ModelForm):
    class Meta:
        model = Review
        fields = ['date', 'rating', 'description']

# Using crispy forms to add date picker and change layout styling
class RentingForm(forms.Form):
    product_id = forms.IntegerField(widget=forms.HiddenInput())
    date_rent = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}), label='Pickup Date:')
    date_return = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}), label='Return Date:')

    helper = FormHelper()
    helper.form_method = 'POST'
    helper.form_action = 'rent_product'
    helper.form_class = 'form-horizontal'
    helper.label_class = 'col-md-3'
    helper.field_class = 'col-md-6'
    helper.layout = Layout(
        Field('date_rent'),
        Field('date_return'),
        FormActions(
            Submit('submit', 'Submit', css_class="btn btn-primary"),
        )
    )

# class CustomUserCreationForm(UserCreationForm):
#     username = forms.CharField(label='username', min_length=5, max_length=150)  
#     email = forms.EmailField(label='email')  
#     password1 = forms.CharField(label='password', widget=forms.PasswordInput)  
#     password2 = forms.CharField(label='Confirm password', widget=forms.PasswordInput)  

#     def username_clean(self):  
#         username = self.cleaned_data['username'].lower()  
#         new = CustomUser.objects.filter(username = username)  
#         if new.count():  
#             raise ValidationError("User Already Exist")  
#         return username
    
#     def email_clean(self):  
#         email = self.cleaned_data['email'].lower()  
#         new = CustomUser.objects.filter(email=email)  
#         if new.count():  
#             raise ValidationError(" Email Already Exist")  
#         return email 

#     def clean_password2(self):  
#         password1 = self.cleaned_data['password1']  
#         password2 = self.cleaned_data['password2']  
  
#         if password1 and password2 and password1 != password2:  
#             raise ValidationError("Password don't match")  
#         return password2  
  
#     def save(self, commit = True):  
#         user = CustomUser.objects.create_user(  
#             self.cleaned_data['username'],  
#             self.cleaned_data['email'],  
#             self.cleaned_data['password1']  
#         )  
#         return user   

User = get_user_model()

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    def clean_username(self):
        username = self.cleaned_data['username'].lower()
        if User.objects.filter(username=username).exists():
            raise ValidationError("Username already exists")
        return username

    def clean_email(self):
        email = self.cleaned_data['email'].lower()
        if User.objects.filter(email=email).exists():
            raise ValidationError("Email already exists")
        return email

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user