from django.forms import ModelForm, inlineformset_factory, HiddenInput
from .models import Review, Renting, Image, Review, Product, CustomUser, RATINGS
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model
from django.utils import timezone
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Field, BaseInput, Div, Hidden
from crispy_forms.bootstrap import FormActions

class UpdateProfileForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name', 'avatar', 'address', 'town', 'county', 'post_code', 'country']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-lg-2'
        self.helper.field_class = 'col-lg-8'
        self.helper.layout = Layout(
            Field('first_name'),
            Field('last_name'),
            Field('avatar'),
            Field('address'),
            Field('town'),
            Field('county'),
            Field('post_code'),
            Field('country'),
            FormActions(
                Div(
                    Submit('submit', 'Save Changes', css_class="btn btn-primary rounded-pill mr-2"),
                    CustomCancel('cancel', 'Cancel', css_class="btn btn-danger rounded-pill"),
                    css_class="d-inline"
                )
            )
        )

# Custom cancel button
class CustomCancel(BaseInput):
    input_type = 'submit'
    field_classes = "d-inline btn btn-danger rounded-pill"

class ImageUploadForm(ModelForm):
    class Meta:
        model = Image
        fields = '__all__'


ImageFormSet = inlineformset_factory(
    Product,
    Image,
    form=ImageUploadForm,
    can_delete=False,
    max_num=1, # Max number of formsets allowed
    extra=1    # Number of formsets to render
)


# Using crispy forms
class ReviewForm(forms.Form):
        date = forms.DateField(widget=forms.HiddenInput(), initial=timezone.now().date())
        rating = forms.ChoiceField(choices=RATINGS)
        description = forms.CharField(
            label='Let us hear your thoughts',
            widget = forms.Textarea()
        )

        helper = FormHelper()
        helper.form_method = 'POST'
        helper.form_action = 'review'
        helper.layout = Layout(
            Field('rating'),
            Field(
                'description',
                  rows='3'
                  ),
            Field('date', type="hidden"),
            FormActions(
                Submit('submit', 'Submit', css_class="btn btn-primary rounded-pill"),
            )
        )

# Using crispy forms
class RentingForm(forms.Form):
    date_rent = forms.DateField(widget=forms.DateInput(attrs={'type': 'text', 'id': 'date_rent'}), label='Pickup Date:')
    date_return = forms.DateField(widget=forms.DateInput(attrs={'type': 'text', 'id': 'date_return'}), label='Return Date:')

    helper = FormHelper()
    helper.form_method = 'POST'
    helper.form_class = 'form-horizontal'
    helper.label_class = 'col-md-3'
    helper.field_class = 'col-md-6'
    helper.layout = Layout(
        Field('date_rent'),
        Field('date_return'),
        FormActions(
            Submit('submit', 'Submit', css_class="btn btn-primary rounded-pill"),
        )
    )

User = get_user_model()

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    helper = FormHelper()
    helper.form_class = 'form-horizontal'
    helper.label_class = 'col-lg-2'
    helper.field_class = 'col-lg-8'
    helper.layout = Layout(
        Field('username'),
        Field('email'),
        Field('password1'),
        Field('password2'),
        FormActions(
            Submit('submit', 'Sign Up', css_class="btn btn-primary rounded-pill"),
        )
    )

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