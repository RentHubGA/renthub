from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('products/', views.ProductList.as_view(), name='product_list'),
    path('reviewform/', views.reviewform, name='reviewform'),
    ## accounts Root
    path('accounts/register/', views.register, name='register'),
]