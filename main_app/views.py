from django.db import transaction
from django.shortcuts import render, redirect
# from django.contrib.auth.forms import UserCreationForm
# import forms.py
from django.shortcuts import get_object_or_404
from django.contrib.auth import login


from django.core.exceptions import PermissionDenied
from django.urls import reverse_lazy
from .forms import CustomUserCreationForm, ReviewForm
from django.views.generic import ListView, DetailView
from django.views.generic.edit import UpdateView
from django.contrib.auth.decorators import login_required
from .models import Product
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import get_user_model

User = get_user_model()

    # path('about', views.about, name='about'),
    # path('products', views.product_index, name='index'),
# Create your views here.

def home(request):
    return render(request, 'home.html')

def about(request):
    return render(request, 'about.html' )

def reviewform(request):
    review_form = ReviewForm
    return render(request, 'review_form.html', {
        'review_form': review_form
    })

# Profile Detail (LoginRequiredMixin)
class ProfileDetailView(LoginRequiredMixin, DetailView):
    model = User
    template_name = 'profile/profile_detail.html'
    context_object_name = 'profile'

    # # Prevent other users from accessing profiles that do not belong to them.
    def get_object(self, queryset=None):
        # Get the requested profile or raise a 404 error if not found
        profile = get_object_or_404(User, pk=self.kwargs['pk'])
        print('User: ', User)
        # Check if the authenticated user is owner  profile
        # profile.user != self.request.user
        print(self.request.user)
        if profile != self.request.user:
            print('profile: ', profile)
            print('self.request.user: ', self.request.user)
            # return PermissionDenied("permission Denied to views profile.")
            raise PermissionDenied("permission Denied to views profile.")
        print('Profile: ', profile)

        return profile
    
# Profile Edit (LoginRequiredMixin)
class ProfileUpdate(LoginRequiredMixin, UpdateView):
    model = User
    template_name = 'profile/profile_form.html'
    fields = ['first_name', 'last_name', 'avatar', 'address', 'town', 'county', 'post_code', 'country']
    success_url = reverse_lazy('profile_detail')

    # Prevent other users from accessing profiles that do not belong to them.
    def get_object(self, queryset=None):
        user = super().get_object(queryset=queryset)
        print('user: ', user)
        if user != self.request.user:
            raise PermissionDenied("permission Denied to update profile.")
        return user
    
    # Redirect to detail page
    # https://docs.djangoproject.com/en/5.0/ref/urlresolvers/#reverse-lazy
    def get_success_url(self):
        return reverse_lazy('profile_detail', kwargs={'pk': self.object.pk})





# @transaction.atomic block unSucceeds create user to database
@transaction.atomic
def register(request):
    error_message = ''

    if request.method == 'POST':  
        form = CustomUserCreationForm(request.POST)  
        if form.is_valid():  
            form.save()
            # if user successful redirect to home page
            return redirect('login')
        else:
            # if not show error message or read error in terminal >> print(form.errors)
            print(form.errors)
            error_message = 'Invalid sign up - try again'
    else:
        form = CustomUserCreationForm()   

    context = {  
        'form':form,
        'error_message': error_message  
    }  
    return render(request, 'registration/signup.html', context)  

# def register(request):
#     error_message = ''

#     if request.method == 'POST':
#         form = CustomUserCreationForm(request.POST)
#         if form.is_valid():
#             user = form.save()
#             login(request, user)  # Log in the user after registration
#             return redirect('home')
#         else:
#             # print(form.errors)
#             error_message = 'Invalid sign up - try again'
#     else:
#         form = CustomUserCreationForm()

#     context = {
#         'form': form,
#         'error_message': error_message
#     }
#     return render(request, 'registration/signup.html', context)

### Products Views ###
# Function Based
# def product_list(request):
# 	products = Product.objects.all()
# 	return render(request, 'products/product_list.html', {
#         'products': products
# 	})

# Class Based
class ProductList(ListView):
    model = Product
    
class ProductDetail(DetailView):
    model = Product