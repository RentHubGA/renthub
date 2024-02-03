# from django import forms  
# # from django.contrib.auth.models import User  
# from django.contrib.auth.forms import UserCreationForm  
# from django.core.exceptions import ValidationError  
# from django.forms.fields import EmailField  
# from django.forms.forms import Form  
from django.forms import ModelForm
from .models import Review

# from .models import Review, CustomUser

# from django.contrib.auth import get_user_model
# User = get_user_model()

class ReviewForm(ModelForm):
    class Meta:
        model = Review
        fields = ['date', 'rating', 'description']




from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model

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
