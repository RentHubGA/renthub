from django.db import transaction
from django.urls import reverse, reverse_lazy
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, get_user_model
from .forms import CustomUserCreationForm, ReviewForm, RentingForm, ImageUploadForm, ImageFormSet
from django.core.exceptions import PermissionDenied
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, FormView, TemplateView
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Product, Image, Renting, Category
from main_app.templatetags.user_dashboard import user_products, user_rent
from django.utils import timezone


import os
import boto3
import uuid

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
    model = User
    template_name = 'profile/profile_form.html'
    fields = ['first_name', 'last_name', 'avatar', 'address', 'town', 'county', 'post_code', 'country']
    success_url = reverse_lazy('profile_detail')

    # Prevent other users from accessing profiles that do not belong to them.
    def get_object(self, queryset=None):
        username = self.kwargs['username']
        user = get_object_or_404(User, username=username)
        print('user: ', user)
        print('username: ', username)
        if user != self.request.user:
            raise PermissionDenied("permission Denied to update profile.")
        return user
    
    # Redirect to detail page
    # https://docs.djangoproject.com/en/5.0/ref/urlresolvers/#reverse-lazy
    def get_success_url(self):
        return reverse_lazy('profile_detail', kwargs={'username': self.object.username})

    
# Profile Dashboard (LoginRequiredMixin)
class ProfileDashboard(LoginRequiredMixin, TemplateView):
    template_name = 'profile/profile_dashboard.html'

    def get(self, request, username):
        user = User.objects.get(username=username)
        products = user_products(user)
        rent = user_rent(user)
        now = timezone.now()
        product_ids = products.values_list('id', flat=True)
        # rented_product_ids = Renting.objects.filter(product_id=product_ids)
        # print(user)
        rented_product_ids = Renting.objects.filter(product__id__in=product_ids).values_list('product__id', flat=True)
        # print(products)
        # print(rent)
        # print(now)
        print(product_ids)
        print(rented_product_ids)
        context = {
            'user': user,
            'products': products,
            'rent': rent,
            'now': now,
            'rented_product_ids': rented_product_ids,

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
    model = Product
    model2 = Category
    
    # def filter_products(request):
    #     product = Product.objects.all()
    #     categories_filter = request.GET.get('categories-filter')
    #     min_filter = request.get('min')
    #     max_filter = request.get('max')

    #     return render(request, "product_list", {
    #         'product': product,
    #     })
    
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
        # TODO: render message for booking requests e.g. 'Success!' or 'Dates not available'
        # context['message'] = message
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
        total_price = product.total_price(date_rent, date_return)
        if product.is_available(date_rent, date_return):
            Renting.objects.create(product=product, user=request.user, date_rent=date_rent, date_return=date_return, total_price=total_price)
            messages.success(request, 'Your booking was successful!')
        else:
            messages.error(request, 'Those dates are unavailable. Please try again.')
    else:
        messages.error(request, 'Invalid form data. Please try again.')
    return redirect('product_detail', pk=pk)
