from typing import Any
from django.db import transaction
from django.urls import reverse, reverse_lazy
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, get_user_model
from .forms import CustomUserCreationForm, ReviewForm, RentingForm, ImageUploadForm, ImageFormSet, UpdateProfileForm
from django.core.exceptions import PermissionDenied
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, View, TemplateView
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Product, Image, Renting, Category, CustomUser, Review
from main_app.templatetags.user_dashboard import user_products, user_rent
from django.utils import timezone
from django.db.models import Q
from django.db.models import Sum
from django.http import JsonResponse
from datetime import datetime, timedelta

import os
import boto3
import uuid

# retrieves the user model active
User = get_user_model()

# path('about', views.about, name='about'),
# path('products', views.product_index, name='index'),
# Create your views here.

def home(request):
    return render(request, 'home.html')

def about(request):
    return render(request, 'about.html' )

def terms(request):
    return render(request, 'terms.html')

# Leave a review
class ReviewCreate(LoginRequiredMixin, View):
    def get(self, request, pk):
# instantiating Review Form Class and passing the form to be rendered
        form = ReviewForm()
        context = {'form': form}
        return render(request, 'review_form.html', context)
# take all the information provided in the form, validates and creates a review in Review model.
    def post(self, request, pk):
        form = ReviewForm(request.POST)
        if form.is_valid():
            date = form.cleaned_data['date']
            rating = form.cleaned_data['rating']
            description = form.cleaned_data['description']
            product = Product.objects.get(pk=pk)
            user_reviews = Review.objects.filter(user=request.user, product=product)
            if user_reviews.exists():
                messages.error(request, 'You have already left a review for this listing.')
                return redirect('review_create', pk=pk)
            elif product.user == request.user:
                messages.error(request, 'You cannot leave a review for your own listing.')
                return redirect('review_create', pk=pk)
            else:
                review = Review.objects.create(
                    date=date,
                    rating=rating,
                    description=description,
                    user=request.user,
                    product_id=pk
                )
                review.save()
                messages.success(request, 'Thank you for your review!')
                return redirect('review_create', pk=pk)
        else:
            messages.error(request, 'Error. Please try again.')
        context = {'form': form}
        return render(request, 'review_form.html', context)

# Profile Detail (LoginRequiredMixin)
class ProfileDetailView(LoginRequiredMixin, DetailView):
    model = User
    template_name = 'profile/profile_detail.html'
    context_object_name = 'profile'

#  Prevent other users from accessing profiles that do not belong to them.
    def get_object(self, queryset=None):
        # Get the requested profile or raise a 404 error if not found
        profile = get_object_or_404(User, username=self.kwargs['username'])
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
    model = CustomUser
    template_name = 'profile/profile_form.html'
    form_class = UpdateProfileForm
    success_url = reverse_lazy('profile_detail')

    def get_object(self, queryset=None):
        username = self.kwargs['username']
        user = get_object_or_404(CustomUser, username=username)
        if user != self.request.user:
            raise PermissionDenied("Permission Denied to update profile.")
        return user
    
    # Redirect to detail page
    # https://docs.djangoproject.com/en/5.0/ref/urlresolvers/#reverse-lazy
    def get_success_url(self):
        return reverse_lazy('profile_detail', kwargs={'username': self.object.username})

    
# Profile Dashboard (LoginRequiredMixin)
class Profile(LoginRequiredMixin, TemplateView):
    template_name = 'profile/profile.html'

    def get(self, request, username):
        user = User.objects.get(username=username)
        products = user_products(user)
        rent = user_rent(user)
        now = timezone.now()
        product_ids = products.values_list('id', flat=True)
        # rented_product_ids = Renting.objects.filter(product_id=product_ids)
        rented_product_ids = Renting.objects.filter(product__id__in=product_ids).values_list('product__id', flat=True)
        
        # for product in products:
        #     print(product.renting_set.all())
        context = {
            'user': user,
            'products': products,
            'rent': rent,
            'now': now,
            'rented_product_ids': rented_product_ids,

            }
        return render(request, self.template_name, context)


# Profile Dashboard (LoginRequiredMixin)
class ProfileDashboard(LoginRequiredMixin, TemplateView):
    template_name = 'profile/profile_dashboard.html'
    def get(self, request, username):
        
        print('User:', username)
        if username != request.user.username:
            raise PermissionDenied("Permission to access this page.")
        user = User.objects.get(username=username)
        products = user_products(user)
        rent = user_rent(user)
        now = timezone.now()
        product_ids = products.values_list('id', flat=True)
        # rented_product_ids = Renting.objects.filter(product_id=product_ids)
        rented_product_ids = Renting.objects.filter(product__id__in=product_ids).values_list('product__id', flat=True)
        # filter Renting by 
        total_rentings = Renting.objects.filter(product__in=products).count()
        latest_renting = Renting.objects.filter(product__in=products).last()
        # latest_renting = Renting.objects.filter(product__in=products).order_by('-date_rent').first()
        current_user = request.user
        print('user ', user)
        print('current_user ', current_user)
        # Calculate total outcome from the current user's rented products
        
        total_outcome = 0
        rent_out_filter = Renting.objects.filter(user=current_user)
        for renting in rent_out_filter:
            total_outcome += renting.total_price
        
        total_income = 0
        rent_in_filter = Renting.objects.filter(product__in=products)
        for renting in rent_in_filter:
            total_income += renting.total_price

        # Total Balance
        total = total_income - total_outcome
        context = {
            'user': user,
            'products': products,
            'rent': rent,
            'now': now,
            'rented_product_ids': rented_product_ids,
            'total_rentings': total_rentings,
            'latest_renting': latest_renting,
            'total_income': total_income,
            'total_outcome': total_outcome,
            'total': total
            }
        return render(request, self.template_name, context)

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


def add_image(request, product_id):
    photo_file = request.FILES.get('photo-file', None)
    if photo_file:
        s3 = boto3.client('s3')
        key = uuid.uuid4().hex[:6] + photo_file.name[photo_file.name.rfind('.'):]
        try:
            bucket = os.environ['S3_BUCKET']
            s3.upload_fileobj(photo_file, bucket, key)
            url = f"{os.environ['S3_BASE_URL']}{bucket}/{key}"
            Image.objects.create(url=url, product_id=product_id)
        except Exception as e:
            print('An error occurred uploading file to S3')
            print(e)
    return redirect('product_detail', product_id=product_id)


class ProductList(ListView):
    paginate_by = 9
    model = Product
    template_name = 'main_app/product_list.html'

    # to display the categories
    def get_queryset(self):
        queryset = super().get_queryset()
        categories_filter = self.request.GET.getlist('categories-filter')
        min_value = self.request.GET.get('min')
        max_value = self.request.GET.get('max')
        search = self.request.GET.get('query')

# ------------- FILTER BY -------------------- #
        
        if min_value == '' or min_value is None:
            min_value = 0
        if max_value == '' or max_value is None:
            max_value = 100000
   
        if len(categories_filter) != 0:
            queryset = queryset.filter(category__name__in=categories_filter)
            if min_value != 0 or max_value != 100000:
                queryset = queryset.filter(Q(price__gte=min_value)& Q(price__lte=max_value))
        elif min_value != 0 or max_value != 100000:
            queryset = queryset.filter(Q(price__gte=min_value)& Q(price__lte=max_value))

# ------------- SEARCH -------------------- #

        if search:
            queryset = queryset.filter(product_name__icontains=search)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        categories = Category.objects.all()
        if not context['object_list']:
            context['no_results'] = "No products match your search."
        context['categories'] = categories
        return context
    

class ProductDetail(DetailView):
    model = Product
    template_name = 'main_app/product_detail.html'
    context_object_name = 'product'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Determines whether the user is the owner of the product
        product = get_object_or_404(Product, id=self.kwargs['pk'])
        is_owner = None
        if self.request.user == product.user:
            is_owner = product.user
        context['reviews'] = self.object.review_set.all()
        context['images'] = self.object.image_set.all()
        context['form'] = RentingForm()
        context['is_owner'] = is_owner
        return context


class ProductCreate(CreateView):
    model = Product
    fields = ['product_name', 'description', 'price', 'category']
    success_url = '/products'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.POST:
            context['image_form'] = ImageFormSet(self.request.POST, self.request.FILES)
        else:
            context['image_form'] = ImageFormSet()

        return context
     
    
    def form_valid(self, form):
        # Assign the logged in user (self.request.user)
        form.instance.user = self.request.user  

        context = self.get_context_data()
        image_form = context['image_form']

        with transaction.atomic():
            self.object = form.save()
            if image_form.is_valid():
                image_form.instance = self.object
                image_form.save()

        return super().form_valid(form)

    
class ProductUpdate(UpdateView):
    model = Product
    fields = ['product_name', 'description', 'price', 'category']
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.POST:
            context['image_form'] = ImageFormSet(self.request.POST, self.request.FILES)
        else:
            context['image_form'] = ImageFormSet()

        return context
    
    def form_valid(self, form):
        # Assign the logged in user (self.request.user)
        form.instance.user = self.request.user  

        context = self.get_context_data()
        image_form = context['image_form']

        with transaction.atomic():
            self.object = form.save()
            if image_form.is_valid():
                image_form.instance = self.object
                image_form.save()

        return super().form_valid(form)

    def get_success_url(self):
        return reverse('product_detail', kwargs={'pk': self.object.id})

class ProductDelete(DeleteView):
    model = Product
    success_url = '/products'


@transaction.atomic
def rent_product(request, pk):
    product = get_object_or_404(Product, id=pk)
    form = RentingForm(request.POST)
    if form.is_valid():
        data = form.cleaned_data
        date_rent = data['date_rent']
        date_return = data['date_return']
        # Check that pickup date is not in the past
        if date_rent < timezone.now().date():
            messages.error(request, 'This date has already passed. Please change the dates and try again.')
            return redirect('product_detail', pk=pk)

        # Handle errors if user sets pickup date to be AFTER drop off date
        if date_return < date_rent:
            messages.error(request, 'Return date cannot be before pickup date.')
            return redirect('product_detail', pk=pk)
        # Calculate total price of booking using total_price method
        total_price = product.total_price(date_rent, date_return)
        # Check availability of product using is_available method
        if product.is_available(date_rent, date_return):
            Renting.objects.create(
                product=product,
                user=request.user,
                date_rent=date_rent,
                date_return=date_return,
                total_price=total_price
                )
            messages.success(request, 'Your booking was successful!')
            return redirect('product_detail', pk=pk)
        else:
            messages.error(request, 'Those dates are unavailable. Please try again.')
            return redirect('product_detail', pk=pk)
    else:
        messages.error(request, 'Invalid form data. Please try again.')
    return redirect('product_detail', pk=pk)

def items(request):
    items = Product.objects.filter()

    return render(request, )

# Fetch unavailable dates
def get_unavailable_dates(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    check_from = datetime.now().date()
    check_to = check_from + timedelta(days=365)
    # Find all bookings between today and 1 year from today
    all_rentings = Renting.objects.filter(
        product=product,
        date_rent__gte=check_from,
        date_return__lte=check_to
    )
    # Iterate through each booking, appending each day it is rented to unavailable_dates
    unavailable_dates = []
    for renting in all_rentings:
        current_date = renting.date_rent
        while current_date <= renting.date_return:
            unavailable_dates.append(current_date.strftime('%Y-%m-%d'))
            current_date += timedelta(days=1)

    return JsonResponse({'unavailable_dates': unavailable_dates})