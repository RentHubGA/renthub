# from django.contrib.auth.models import User  
# from django.forms.fields import EmailField  
# from django.forms.forms import Form  
from django.forms import ModelForm, inlineformset_factory
from .models import Review, Renting, Image, Review, Product
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Field
from crispy_forms.bootstrap import FormActions

class ImageUploadForm(ModelForm):
    class Meta:
        model = Image
        fields = '__all__'

ImageFormSet = inlineformset_factory(
    Product,
    Image,
    form=ImageUploadForm,
    can_delete=False,
    max_num=5, # Max number of formsets allowed
    extra=1    # Number of formsets to render
)

# from .models import Review, CustomUser

# from django.contrib.auth import get_user_model
# User = get_user_model()


class ReviewForm(ModelForm):
    class Meta:
        model = Review
        fields = ['date', 'rating', 'description']


# Using crispy forms to add date picker and change layout styling
class RentingForm(forms.Form):
    date_rent = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}), label='Pickup Date:')
    date_return = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}), label='Return Date:')

    helper = FormHelper()
    helper.form_method = 'POST'
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