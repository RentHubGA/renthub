from django.db import transaction
from django.shortcuts import render, redirect, get_object_or_404
# from django.contrib.auth.forms import UserCreationForm
# import forms.py
from .forms import CustomUserCreationForm, ReviewForm
from django.contrib.auth import login
from django.views.generic import ListView, DetailView
from django.contrib.auth.decorators import login_required
from .models import Product

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
    template_name = 'main_app/product_detail.html'
    context_object_name = 'product'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['reviews'] = self.object.review_set.all()
        context['images'] = self.object.image_set.all()
        return context